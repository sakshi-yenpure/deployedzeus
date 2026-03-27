import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, TrendingUp, TrendingDown, Minus, Info, BarChart2, Star, RefreshCw, Download } from 'lucide-react';

const QualityContainer = styled.div`
  width: 100%;
  padding: 1rem 0;
  min-height: 80vh;
`;

const PageHeader = styled(motion.div)`
  margin-bottom: 3rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
`;

const RefreshButton = styled(motion.button)<{ isLoading?: boolean }>`
  position: absolute;
  top: 0;
  right: 0;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: rgba(0, 242, 254, 0.1);
  border: 1px solid rgba(0, 242, 254, 0.2);
  color: #00f2fe;
  padding: 0.8rem 1.4rem;
  border-radius: 100px;
  font-weight: 700;
  font-size: 0.8rem;
  cursor: ${props => props.isLoading ? 'not-allowed' : 'pointer'};
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);

  &:hover {
    background: rgba(0, 242, 254, 0.2);
    border-color: rgba(0, 242, 254, 0.4);
    box-shadow: 0 0 20px rgba(0, 242, 254, 0.2);
  }

  svg {
    animation: ${props => props.isLoading ? 'spin 2s linear infinite' : 'none'};
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  @media (max-width: 768px) {
    position: static;
    margin-bottom: 1.5rem;
  }
`;

const DownloadButton = styled(motion.button)`
  position: absolute;
  top: 55px;
  right: 0;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
  padding: 0.8rem 1.4rem;
  border-radius: 100px;
  font-weight: 700;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
  }

  @media (max-width: 768px) {
    position: static;
    margin-bottom: 1.5rem;
  }
`;

const Title = styled.h1`
  font-size: 3.5rem;
  font-weight: 950;
  letter-spacing: -2px;
  background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
`;

const Subtitle = styled.p`
  color: ${props => props.theme.colors.textSecondary};
  font-size: 1.1rem;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
`;

const SectorGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 2rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const SectorCard = styled(motion.div)`
  background: ${props => props.theme.colors.cardBackground};
  backdrop-filter: blur(20px);
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 24px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #00f2fe, #7028e4);
    opacity: 0.6;
  }
`;

const SectorHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
`;

const SectorName = styled.h2`
  font-size: 1.5rem;
  font-weight: 800;
  text-transform: capitalize;
  color: #fff;
`;

const MetadataBadge = styled.span`
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
`;

const ReportSection = styled.div`
  background: rgba(255, 255, 255, 0.03);
  border-radius: 16px;
  padding: 1.2rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
`;

const ReportTitle = styled.h3`
  font-size: 0.9rem;
  font-weight: 700;
  color: #00f2fe;
  margin-bottom: 0.8rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const HeadlineList = styled.ul`
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
`;

const HeadlineItem = styled.li`
  font-size: 0.85rem;
  line-height: 1.4;
  color: rgba(255, 255, 255, 0.7);
  padding-left: 1.2rem;
  position: relative;

  &::before {
    content: '•';
    position: absolute;
    left: 0;
    color: #00f2fe;
  }
`;

const TopStocksSection = styled.div``;

const TopStocksTitle = styled.h3`
  font-size: 0.9rem;
  font-weight: 700;
  color: #fff;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const StockList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
`;

const StockItem = styled(motion.div)`
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid rgba(255, 255, 255, 0.05);
`;

const StockInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
`;

const StockSymbol = styled.div`
  font-weight: 800;
  font-size: 1rem;
  color: #fff;
`;

const ClassificationBadge = styled.span<{ type: string }>`
  padding: 0.25rem 0.6rem;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  background: ${props => 
    props.type === 'Bullish' || props.type.includes('Positive') ? 'rgba(0, 255, 163, 0.15)' : 
    props.type === 'Bearish' || props.type.includes('Negative') ? 'rgba(255, 46, 99, 0.15)' : 'rgba(255, 193, 7, 0.15)'};
  color: ${props => 
    props.type === 'Bullish' || props.type.includes('Positive') ? '#00ffa3' : 
    props.type === 'Bearish' || props.type.includes('Negative') ? '#ff2e63' : '#ffc107'};
`;

const ScoreWrapper = styled.div`
  text-align: right;
`;

const ScoreValue = styled.div<{ positive: boolean }>`
  font-weight: 900;
  font-size: 1rem;
  font-family: 'JetBrains Mono', monospace;
  color: ${props => props.positive ? '#00ffa3' : '#ff2e63'};
`;

const LoadingOverlay = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400px;
  width: 100%;
  color: #00f2fe;
  font-weight: 700;
`;

interface Stock {
  symbol: string;
  name: string;
  score: number;
  classification: string;
  confidence: number;
  prediction: string;
}

interface SectorReport {
  sector: string;
  top_stocks: Stock[];
  headlines: { headline: string; source: string; classification: string }[];
  metadata: { analysis_timestamp: string; method: string };
}

const Quality: React.FC = () => {
  const [reports, setReports] = useState<SectorReport[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchReport = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/chat/quality-report/');
      const data = await response.json();
      if (data.success) {
        setReports(data.report);
      } else {
        setError(data.message || 'Failed to load report');
      }
    } catch (err) {
      setError('Connection error. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReport();
  }, []);

  const handleRefresh = async () => {
    if (refreshing) return;
    setRefreshing(true);
    try {
      const response = await fetch('http://localhost:8000/api/chat/refresh-quality-report/', {
        method: 'POST'
      });
      const data = await response.json();
      if (data.success) {
        setReports(data.report);
      } else {
        alert('Failed to refresh: ' + (data.message || 'Unknown error'));
      }
    } catch (err) {
      alert('Connection error during refresh.');
    } finally {
      setRefreshing(false);
    }
  };

  const handleDownload = () => {
    window.open('http://localhost:8000/api/chat/download-quality-report/', '_blank');
  };

  if (loading) return <LoadingOverlay>Analyzing Market Quality...</LoadingOverlay>;
  if (error) return <LoadingOverlay style={{ color: '#ff2e63' }}>{error}</LoadingOverlay>;

  return (
    <QualityContainer>
      <PageHeader
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <RefreshButton 
          onClick={handleRefresh} 
          isLoading={refreshing}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <RefreshCw size={16} />
          {refreshing ? 'Analyzing Market...' : 'Refresh Analysis'}
        </RefreshButton>
        <DownloadButton
          onClick={handleDownload}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Download size={16} />
          Download CSV
        </DownloadButton>
        <Title>QUALITY REPORT</Title>
        <Subtitle>
          A comprehensive sentiment analysis of the Indian market. We analyze thousands of news headlines
          to identify high-quality stock opportunities across all major sectors.
        </Subtitle>
      </PageHeader>

      <SectorGrid>
        {reports.map((report, index) => (
          <SectorCard
            key={report.sector}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1, duration: 0.5 }}
          >
            <SectorHeader>
              <SectorName>{report.sector}</SectorName>
              <MetadataBadge>
                {new Date(report.metadata.analysis_timestamp).toLocaleDateString()}
              </MetadataBadge>
            </SectorHeader>

            <ReportSection>
              <ReportTitle>
                <BarChart2 size={16} /> Market Sentiment Report
              </ReportTitle>
              <HeadlineList>
                {report.headlines.slice(0, 3).map((h, i) => (
                  <HeadlineItem key={i}>{h.headline}</HeadlineItem>
                ))}
              </HeadlineList>
            </ReportSection>

            <TopStocksSection>
              <TopStocksTitle>
                <Star size={16} fill="#ffc107" color="#ffc107" /> Premium Picks
              </TopStocksTitle>
              <StockList>
                {report.top_stocks.map((stock) => (
                  <StockItem 
                    key={stock.symbol}
                    whileHover={{ scale: 1.02, backgroundColor: 'rgba(255, 255, 255, 0.08)' }}
                  >
                    <StockInfo>
                      <StockSymbol>{stock.name}</StockSymbol>
                      <ClassificationBadge type={stock.prediction}>
                        {stock.prediction}
                      </ClassificationBadge>
                    </StockInfo>
                    <ScoreWrapper>
                      <ScoreValue positive={stock.score >= 0}>
                        {stock.score > 0 ? '+' : ''}{(stock.score * 100).toFixed(1)}%
                      </ScoreValue>
                      <div style={{ fontSize: '0.65rem', color: 'rgba(255,255,255,0.4)', fontWeight: 600 }}>
                        CONFIDENCE: {stock.confidence}%
                      </div>
                    </ScoreWrapper>
                  </StockItem>
                ))}
              </StockList>
            </TopStocksSection>
          </SectorCard>
        ))}
      </SectorGrid>
    </QualityContainer>
  );
};

export default Quality;
