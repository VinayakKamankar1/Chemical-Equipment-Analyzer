import React, { useState, useEffect } from 'react';
import CSVUpload from './CSVUpload';
import DataVisualization from './DataVisualization';
import History from './History';
import { getHistory } from '../utils/api';
import './Dashboard.css';

const Dashboard = ({ onLogout }) => {
  const [currentData, setCurrentData] = useState(null);
  const [history, setHistory] = useState([]);
  const [activeTab, setActiveTab] = useState('upload');

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await getHistory();
      setHistory(data);
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  const handleUploadSuccess = (data) => {
    setCurrentData(data);
    setActiveTab('visualization');
    loadHistory();
  };

  const handleViewHistoryItem = (item) => {
    setCurrentData(item);
    setActiveTab('visualization');
  };

  return (
    <div className="dashboard">
      <div className="header">
        <h1>Chemical Equipment Analyzer</h1>
        <button onClick={onLogout} className="btn btn-danger">
          Logout
        </button>
      </div>

      <div className="container">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'upload' ? 'active' : ''}`}
            onClick={() => setActiveTab('upload')}
          >
            Upload CSV
          </button>
          <button
            className={`tab ${activeTab === 'visualization' ? 'active' : ''}`}
            onClick={() => setActiveTab('visualization')}
            disabled={!currentData}
          >
            Visualization
          </button>
          <button
            className={`tab ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            History
          </button>
        </div>

        {activeTab === 'upload' && (
          <CSVUpload onUploadSuccess={handleUploadSuccess} />
        )}

        {activeTab === 'visualization' && currentData && (
          <DataVisualization data={currentData} />
        )}

        {activeTab === 'history' && (
          <History
            history={history}
            onViewItem={handleViewHistoryItem}
            onRefresh={loadHistory}
          />
        )}
      </div>
    </div>
  );
};

export default Dashboard;

