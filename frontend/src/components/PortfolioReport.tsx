import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Download, FileText } from 'lucide-react';
import { PortfolioItem } from '../contexts/AuthContext';

const ReportCard = styled(motion.div)`
  background: ${props => props.theme.colors.cardBackground};
  border-radius: ${props => props.theme.borderRadius.large};
  border: 1px solid ${props => props.theme.colors.border};
  padding: 2.5rem;
  margin-bottom: 4rem;
  backdrop-filter: blur(12px);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  }
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;

  @media (max-width: 640px) {
    flex-direction: column;
    align-items: flex-start;
    gap: 1.5rem;
  }
`;

const Title = styled.h2`
  font-size: 1.8rem;
  font-weight: 800;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  letter-spacing: -0.5px;
`;

const DownloadButton = styled(motion.button)`
  display: flex;
  align-items: center;
  gap: 0.6rem;
  background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
  border: none;
  color: #000;
  padding: 0.7rem 1.4rem;
  border-radius: 12px;
  font-weight: 800;
  font-size: 0.8rem;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(0, 242, 254, 0.2);
  text-transform: uppercase;
  letter-spacing: 0.5px;

  &:hover {
    filter: brightness(1.1);
  }
`;

const TableContainer = styled.div`
  overflow-x: auto;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.08);

  &::-webkit-scrollbar {
    height: 6px;
  }
  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 10px;
  }
`;

const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  color: #fff;
  min-width: 800px;
`;

const Th = styled.th`
  text-align: left;
  padding: 1.2rem 1.5rem;
  background: rgba(255, 255, 255, 0.03);
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
`;

const Td = styled.td`
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 0.95rem;
  vertical-align: middle;
`;

const Symbol = styled.span`
  font-family: 'JetBrains Mono', monospace;
  font-weight: 800;
  color: #00f2fe;
  font-size: 1rem;
`;

const Price = styled.span`
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  color: #fff;
`;

const Change = styled.span<{ positive: boolean }>`
  background: ${props => props.positive ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)'};
  color: ${props => props.positive ? '#10b981' : '#ef4444'};
  padding: 0.3rem 0.7rem;
  border-radius: 8px;
  font-weight: 800;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
`;

const SectorBadge = styled.span`
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.8);
  padding: 0.3rem 0.7rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
`;

interface PortfolioReportProps {
  portfolio: PortfolioItem[];
}

const PortfolioReport: React.FC<PortfolioReportProps> = ({ portfolio }) => {
  const [sentiments, setSentiments] = useState<{ [symbol: string]: any }>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSentiments = async () => {
      try {
        setLoading(true);
        // Use relative URL to avoid localhost mismatch
        const response = await fetch('/api/chat/all-stock-sentiment/');
        if (!response.ok) throw new Error('Network response was not ok');
        const result = await response.json();
        
        if (result.success && result.stocks) {
          // Normalize keys to uppercase for better matching
          const normalized: { [key: string]: any } = {};
          Object.keys(result.stocks).forEach(k => {
            normalized[k.toUpperCase()] = result.stocks[k];
          });
          setSentiments(normalized);
          console.log('Successfully loaded sentiments for', Object.keys(normalized).length, 'stocks');
        }
      } catch (err) {
        console.error('Failed to fetch sentiments:', err);
        // Fallback to absolute if relative fails (for local dev)
        try {
          const response = await fetch('http://localhost:8000/api/chat/all-stock-sentiment/');
          const result = await response.json();
          if (result.success) {
            const normalized: { [key: string]: any } = {};
            Object.keys(result.stocks).forEach(k => {
                normalized[k.toUpperCase()] = result.stocks[k];
            });
            setSentiments(normalized);
          }
        } catch (e2) {
          console.error('Final fallback fetch failed:', e2);
        }
      } finally {
        setLoading(false);
      }
    };
    fetchSentiments();
  }, []);

  const getSentimentForSymbol = (symbol: string) => {
    const s = symbol.toUpperCase();
    // Try exact match
    if (sentiments[s]) return sentiments[s];
    
    // Try without .NS
    const s2 = s.replace('.NS', '');
    if (sentiments[s2]) return sentiments[s2];
    
    // Try finding by prefix (helpful for spelling variants like Waaree)
    const partialMatch = Object.keys(sentiments).find(k => 
      k.startsWith(s2.substring(0, 5)) || s2.startsWith(k.replace('.NS', '').substring(0, 5))
    );
    if (partialMatch) return sentiments[partialMatch];

    return null;
  };

  const handleDownload = () => {
    const headers = ['Symbol', 'Name', 'Sector', 'Current Price', 'Sentiment Score', 'Classification', 'Prediction', 'Date Added'];
    const rows = portfolio.map(item => {
      const sentiment = getSentimentForSymbol(item.symbol) || {};
      return [
        item.symbol,
        item.name.replace(/,/g, ''),
        item.sector || 'N/A',
        item.price.toFixed(2),
        sentiment.overall_score !== undefined ? sentiment.overall_score.toFixed(4) : 'N/A',
        sentiment.classification || 'Neutral',
        sentiment.prediction || 'Neutral',
        new Date(item.addedAt).toLocaleDateString()
      ];
    });

    const csvContent = headers.join(',') + '\n' + rows.map(r => r.join(',')).join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `Zeus_Institutional_Portfolio_Report_${new Date().toLocaleDateString().replace(/\//g, '-')}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (portfolio.length === 0) return null;

  return (
    <ReportCard
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6 }}
    >
      <Header>
        <Title>
          <FileText size={24} color="#00f2fe" style={{ filter: 'drop-shadow(0 0 8px rgba(0, 242, 254, 0.4))' }} />
          Portfolio Institutional Report
        </Title>
        <DownloadButton
          onClick={handleDownload}
          whileHover={{ scale: 1.05, y: -2 }}
          whileTap={{ scale: 0.95 }}
        >
          <Download size={18} />
          Download Report
        </DownloadButton>
      </Header>

      <TableContainer>
        <Table>
          <thead>
            <tr>
              <Th>Asset</Th>
              <Th>Sector</Th>
              <Th>Market Price</Th>
              <Th>Sentiment Performance</Th>
              <Th>Registry Date</Th>
            </tr>
          </thead>
          <tbody>
            {portfolio.map((item) => {
              const sentiment = getSentimentForSymbol(item.symbol) || { overall_score: 0, classification: 'Neutral', prediction: 'Neutral' };
              const score = sentiment.overall_score || 0;
              const isPositive = score > 0;
              const isNeutral = score === 0 || (score > -0.05 && score < 0.05);

              return (
                <tr key={item.symbol}>
                  <Td>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                      <Symbol>{item.symbol}</Symbol>
                      <span style={{ fontSize: '0.8rem', color: 'rgba(255,255,255,0.4)', fontWeight: 600 }}>{item.name}</span>
                    </div>
                  </Td>
                  <Td>
                    <SectorBadge>{item.sector || 'uncategorized'}</SectorBadge>
                  </Td>
                  <Td><Price>${item.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</Price></Td>
                  <Td>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                      <Change positive={score >= 0} style={{ 
                        background: isNeutral ? 'rgba(148, 163, 184, 0.1)' : undefined,
                        color: isNeutral ? '#94a3b8' : undefined
                      }}>
                        {score > 0 ? '▲' : score < 0 ? '▼' : '▬'} {sentiment.classification}
                      </Change>
                      <span style={{ fontSize: '0.7rem', color: 'rgba(255,255,255,0.3)', fontWeight: 700, marginLeft: '4px' }}>
                        SCORE: {score.toFixed(4)}
                      </span>
                    </div>
                  </Td>
                  <Td>
                    <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: '0.85rem', fontWeight: 600 }}>
                      {new Date(item.addedAt).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                    </span>
                  </Td>
                </tr>
              );
            })}
          </tbody>
        </Table>
      </TableContainer>
    </ReportCard>
  );
};

export default PortfolioReport;
