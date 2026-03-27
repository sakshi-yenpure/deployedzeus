"""
ChromaDB Vector Store for Zeus Chatbot.
Indexes the question bank for semantic similarity search.
Falls back gracefully if chromadb is not installed.
"""
import logging
import os

logger = logging.getLogger(__name__)

# ChromaDB collection name
COLLECTION_NAME = "zeus_qa_bank"

# Module-level cache so we initialise only once per server lifetime
_client = None
_collection = None


def _get_collection():
    """Lazily initialise ChromaDB and index the question bank."""
    global _client, _collection
    if _collection is not None:
        return _collection

    try:
        import chromadb
        from .question_bank import ALL_QA_PAIRS

        # Use persistent client (saves data to disk)
        persist_directory = os.path.join(os.path.dirname(__file__), "chroma_db")
        _client = chromadb.PersistentClient(path=persist_directory)

        # For now, always rebuild to ensure question bank updates are Picked up.
        try:
            _client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass

        _collection = _client.create_collection(COLLECTION_NAME)

        # Index all Q&A pairs
        ids = []
        documents = []
        metadatas = []
        for idx, (question, answer) in enumerate(ALL_QA_PAIRS):
            ids.append(str(idx))
            documents.append(question)
            metadatas.append({"answer": answer})

        if ids:
            _collection.add(ids=ids, documents=documents, metadatas=metadatas)

        logger.info(f"ChromaDB: indexed {len(ids)} Q&A pairs into '{COLLECTION_NAME}'")

    except ImportError:
        logger.warning("chromadb not installed — vector similarity search disabled")
        _collection = None
    except Exception as e:
        logger.error(f"ChromaDB init failed: {e}")
        _collection = None

    return _collection


def chroma_search(query: str, threshold: float = 0.35) -> str | None:
    """
    Search ChromaDB for semantically similar questions.
    Returns the stored answer if similarity is above threshold, else None.

    Args:
        query: User's input question
        threshold: Distance threshold — ChromaDB returns l2-distances.
                   Lower distance = more similar.
                   We accept matches where distance < threshold (default 0.35)
    """
    collection = _get_collection()
    if collection is None:
        return None

    try:
        results = collection.query(
            query_texts=[query],
            n_results=1,
        )

        if not results or not results.get("documents"):
            return None

        distances = results.get("distances", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        if not distances or not metadatas:
            return None

        distance = distances[0]
        # ChromaDB l2 distance: 0 = identical, higher = more different
        # Threshold of 0.35 works well for short text similarity
        if distance < threshold:
            answer = metadatas[0].get("answer", "")
            logger.info(f"ChromaDB hit — distance={distance:.3f} for query='{query[:40]}'")
            return answer

        logger.info(f"ChromaDB miss — best distance={distance:.3f} (threshold={threshold})")
        return None

    except Exception as e:
        logger.warning(f"ChromaDB search error: {e}")
        return None


def warm_up():
    """Pre-warm the ChromaDB collection at startup."""
    _get_collection()
