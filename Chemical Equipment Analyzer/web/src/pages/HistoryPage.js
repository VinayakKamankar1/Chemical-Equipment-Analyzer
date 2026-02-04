import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import History from '../components/History';
import { getHistory } from '../utils/api';
import './HistoryPage.css';

const HistoryPage = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await getHistory();
      setHistory(data);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleViewItem = (item) => {
    navigate('/dashboard', { state: { viewData: item } });
  };

  return (
    <div className="history-page">
      <div className="page-header">
        <h2 className="page-title">Upload History</h2>
        <p className="page-subtitle">View and manage your previous data uploads</p>
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading history...</p>
        </div>
      ) : (
        <div className="fade-in">
          <History
            history={history}
            onViewItem={handleViewItem}
            onRefresh={loadHistory}
          />
        </div>
      )}
    </div>
  );
};

export default HistoryPage;

