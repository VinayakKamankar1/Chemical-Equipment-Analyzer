import React from 'react';
import { downloadPDF } from '../utils/api';
import './History.css';

const History = ({ history, onViewItem, onRefresh }) => {
  const handleDownloadPDF = async (e, summaryId) => {
    e.stopPropagation();
    try {
      await downloadPDF(summaryId);
    } catch (error) {
      alert('Failed to download PDF');
    }
  };

  if (history.length === 0) {
    return (
      <div className="card">
        <h2>Upload History</h2>
        <p>No uploads yet. Upload a CSV file to get started.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="history-header">
        <h2>Upload History (Last 5)</h2>
        <button onClick={onRefresh} className="btn btn-secondary">
          Refresh
        </button>
      </div>
      <div className="history-list">
        {history.map((item) => (
          <div
            key={item.id}
            className="history-item"
            onClick={() => onViewItem(item)}
          >
            <h3>{item.filename}</h3>
            <p>
              <strong>Uploaded:</strong>{' '}
              {new Date(item.uploaded_at).toLocaleString()}
            </p>
            <p>
              <strong>Equipment Count:</strong> {item.total_equipment_count}
            </p>
            <p>
              <strong>Avg Flowrate:</strong> {item.avg_flowrate.toFixed(2)} |{' '}
              <strong>Avg Pressure:</strong> {item.avg_pressure.toFixed(2)} |{' '}
              <strong>Avg Temperature:</strong> {item.avg_temperature.toFixed(2)}
            </p>
            <div className="history-actions">
              <button
                onClick={(e) => handleDownloadPDF(e, item.id)}
                className="btn btn-secondary btn-sm"
              >
                Download PDF
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default History;

