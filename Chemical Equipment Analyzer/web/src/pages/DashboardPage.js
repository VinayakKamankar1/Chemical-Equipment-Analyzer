import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import CSVUpload from '../components/CSVUpload';
import DataVisualization from '../components/DataVisualization';
import { getHistory } from '../utils/api';
import './DashboardPage.css';

const DashboardPage = () => {
  const [currentData, setCurrentData] = useState(null);
  const [activeView, setActiveView] = useState('upload');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Check if navigating from history page with data
    if (location.state?.viewData) {
      setCurrentData(location.state.viewData);
      setActiveView('visualization');
    }
  }, [location.state]);

  const handleUploadSuccess = (data) => {
    setCurrentData(data);
    setActiveView('visualization');
  };

  const handleViewHistory = () => {
    navigate('/history');
  };

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h2 className="page-title">Dashboard</h2>
        <p className="page-subtitle">Upload and analyze your chemical equipment data</p>
      </div>

      <div className="dashboard-tabs">
        <button
          className={`dashboard-tab ${activeView === 'upload' ? 'active' : ''}`}
          onClick={() => setActiveView('upload')}
        >
          <span className="tab-icon">📤</span>
          Upload CSV
        </button>
        <button
          className={`dashboard-tab ${activeView === 'visualization' ? 'active' : ''}`}
          onClick={() => setActiveView('visualization')}
          disabled={!currentData}
        >
          <span className="tab-icon">📊</span>
          Visualization
        </button>
        <button
          className="dashboard-tab"
          onClick={handleViewHistory}
        >
          <span className="tab-icon">📜</span>
          View History
        </button>
      </div>

      <div className="dashboard-content">
        {activeView === 'upload' && (
          <div className="fade-in">
            <CSVUpload onUploadSuccess={handleUploadSuccess} />
          </div>
        )}

        {activeView === 'visualization' && currentData && (
          <div className="fade-in">
            <DataVisualization data={currentData} />
          </div>
        )}

        {activeView === 'visualization' && !currentData && (
          <div className="empty-state">
            <div className="empty-icon">📊</div>
            <h3>No Data to Visualize</h3>
            <p>Upload a CSV file to see visualizations</p>
            <button
              className="btn btn-primary"
              onClick={() => setActiveView('upload')}
            >
              Upload CSV File
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;

