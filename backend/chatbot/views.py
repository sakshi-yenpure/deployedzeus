"""
Main chat API endpoint for Zeus AI Chatbot.
Supports public (anonymous) and private (authenticated) modes.
"""
import logging
import uuid
import json
import os
import csv
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse
from users.models import Stock
from users.stock_sentiment import analyze_sector_sentiment

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger(__name__)


def _get_user_from_token(request) -> int | None:
    """Extract user_id from JWT Bearer token if present."""
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return None
    try:
        token_str = auth_header.split(' ', 1)[1]
        token = AccessToken(token_str)
        return token.get('user_id') or token.get('id')
    except Exception:
        return None


@api_view(['POST', 'OPTIONS'])
@permission_classes([AllowAny])
@authentication_classes([])
def chat(request):
    """
    POST /api/chat/
    Body: { "query": str, "session_id": str (optional) }
    Headers: Authorization: Bearer <token>  (optional, enables private mode)
    """
    if request.method == 'OPTIONS':
        return Response(status=status.HTTP_200_OK)

    query = (request.data.get('query') or '').strip()
    session_id = request.data.get('session_id') or str(uuid.uuid4())

    if not query:
        return Response(
            {'success': False, 'message': 'query is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if len(query) > 1000:
        return Response(
            {'success': False, 'message': 'Query too long (max 1000 characters).'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Determine mode
    user_id = _get_user_from_token(request)
    is_private = user_id is not None

    # Save to conversation memory
    try:
        from .memory import get_context, save_turn
        context = get_context(session_id)
    except Exception:
        context = ''
        save_turn = None

    # Run the LangGraph pipeline
    try:
        from .graph import run_graph
        result = run_graph(
            query=query,
            session_id=session_id,
            user_id=user_id,
            is_private=is_private,
        )
    except Exception as e:
        logger.error(f"Graph error: {e}")
        result = {
            'response': (
                "⚡ **Zeus AI Temporarily Unavailable**\n\n"
                "Our AI engine is currently restarting. Please try again in a moment.\n"
                "You can still browse live stock data on the Stocks and Metals pages."
            ),
            'intent': 'error',
            'requires_mpin': False,
            'requires_auth': False,
        }

    response_text = result.get('response', '')
    intent = result.get('intent', 'qa')

    # Save conversation turn to memory
    if save_turn:
        try:
            save_turn(session_id, query, response_text, intent)
        except Exception:
            pass

    # Log to ChatLog table
    try:
        from .models import ChatLog
        ChatLog.objects.create(
            user_id=user_id,
            session_id=session_id,
            query=query,
            response=response_text[:2000],
            intent=intent,
            is_private=is_private,
        )
    except Exception as log_err:
        logger.warning(f"ChatLog save failed: {log_err}")

    return Response({
        'success': True,
        'session_id': session_id,
        'query': query,
        'response': response_text,
        'intent': intent,
        'is_private': is_private,
        'requires_mpin': result.get('requires_mpin', False),
        'requires_auth': result.get('requires_auth', False),
        'action': result.get('action'),
        'symbol': result.get('symbol'),
        'stock_name': result.get('stock_name'),
        'price': result.get('price'),
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def chat_history(request):
    """GET /api/chat/history/?session_id=<id> — returns last 20 messages."""
    session_id = request.query_params.get('session_id')
    if not session_id:
        return Response({'success': False, 'message': 'session_id required'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        from .models import ChatLog
        logs = ChatLog.objects.filter(session_id=session_id).order_by('timestamp')[:20]
        data = [
            {
                'query': log.query,
                'response': log.response,
                'intent': log.intent,
                'timestamp': log.timestamp.isoformat(),
            }
            for log in logs
        ]
        return Response({'success': True, 'history': data})
    except Exception as e:
        return Response({'success': False, 'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def _get_quality_report_processed_data():
    """Helper to load and process the sentiment report JSON."""
    file_path = os.path.join(settings.BASE_DIR, 'sentiment_report.json')
    if not os.path.exists(file_path):
        return None

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        report_data = []
        for sector_name, sector_info in data.items():
            stocks = sector_info.get('stocks', {})
            
            # Rank stocks by overall_score descending, then confidence descending
            sorted_stocks = sorted(
                stocks.items(),
                key=lambda x: (x[1].get('overall_score', 0), x[1].get('confidence', 0)),
                reverse=True
            )

            top_3 = []
            for symbol, details in sorted_stocks[:3]:
                top_3.append({
                    'symbol': symbol,
                    'name': symbol.replace('.NS', ''),
                    'score': details.get('overall_score', 0),
                    'classification': details.get('classification', 'Neutral'),
                    'confidence': details.get('confidence', 0),
                    'prediction': details.get('prediction', 'Neutral')
                })

            report_data.append({
                'sector': sector_name,
                'metadata': sector_info.get('metadata', {}),
                'top_stocks': top_3,
                'headlines': sector_info.get('headlines', [])[:5]
            })
        return report_data
    except Exception as e:
        logger.error(f"Error processing quality report: {e}")
        return None


@api_view(['GET'])
@permission_classes([AllowAny])
def quality_report(request):
    """
    GET /api/chat/quality-report/
    Returns sentiment analysis report for each sector and top 3 stocks.
    """
    report_data = _get_quality_report_processed_data()
    if report_data is None:
        return Response({
            'success': False,
            'message': 'Sentiment report not found or could not be processed.'
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({
        'success': True,
        'report': report_data
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_quality_report(request):
    """
    POST /api/chat/refresh-quality-report/
    Triggers a full sentiment analysis for all sectors and updates sentiment_report.json.
    """
    try:
        sectors = list(Stock.objects.values_list('sector', flat=True).distinct())
        if not sectors:
            return Response({
                'success': False,
                'message': 'No sectors found in database.'
            }, status=status.HTTP_404_NOT_FOUND)

        report = {}
        for sector in sectors:
            try:
                # This performs scraping and analysis which takes time
                sentiment = analyze_sector_sentiment(sector)
                if sentiment and 'stocks' in sentiment:
                    report[sector] = sentiment
            except Exception as e:
                logger.error(f"Error analyzing sector {sector}: {e}")

        if not report:
            return Response({
                'success': False,
                'message': 'Failed to generate any sentiment data.'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Save to JSON
        report_path = os.path.join(settings.BASE_DIR, 'sentiment_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4)

        # Return the processed data immediately after refresh
        report_data = _get_quality_report_processed_data()
        return Response({
            'success': True,
            'report': report_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error refreshing quality report: {e}")
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def download_quality_report(request):
    """
    GET /api/chat/download-quality-report/
    Generates and returns a CSV file of the sentiment report.
    """
    try:
        file_path = os.path.join(settings.BASE_DIR, 'sentiment_report.json')
        if not os.path.exists(file_path):
            return Response({
                'success': False,
                'message': 'Sentiment report not found on server.'
            }, status=status.HTTP_404_NOT_FOUND)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="zeus_quality_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Sector', 'Stock Symbol', 'Overall Score', 'Classification', 'Confidence', 'Top Headlines'])

        for sector, info in data.items():
            stocks = info.get('stocks', {})
            headlines_list = info.get('headlines', [])
            headlines = "; ".join([h.get('headline', '') for h in headlines_list[:3]])
            
            for symbol, details in stocks.items():
                writer.writerow([
                    sector,
                    symbol,
                    details.get('overall_score', 0),
                    details.get('classification', 'Neutral'),
                    details.get('confidence', 0),
                    headlines
                ])
                headlines = ""  # Only show headlines on the first row of each sector
                
        return response

    except Exception as e:
        logger.error(f"Error downloading quality report: {e}")
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def all_stock_sentiment(request):
    """
    GET /api/chat/all-stock-sentiment/
    Returns a unified map of all stocks and their sentiment data.
    """
    try:
        file_path = os.path.join(settings.BASE_DIR, 'sentiment_report.json')
        if not os.path.exists(file_path):
            return Response({
                'success': False,
                'message': 'Sentiment report not found on server.'
            }, status=status.HTTP_404_NOT_FOUND)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        all_stocks = {}
        for sector_info in data.values():
            stocks = sector_info.get('stocks', {})
            for symbol, details in stocks.items():
                all_stocks[symbol] = details
        
        return Response({
            'success': True,
            'stocks': all_stocks
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error fetching all stock sentiment: {e}")
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
