import React from 'react';
import './AboutPage.css';

const AboutPage = () => {
  return (
    <div className="about-page">
      <div className="page-header">
        <h2 className="page-title">About</h2>
        <p className="page-subtitle">Learn more about the Chemical Equipment Analyzer</p>
      </div>

      <div className="about-content">
        <div className="about-card">
          <div className="card-icon">⚗️</div>
          <h3>What is this?</h3>
          <p>
            Chemical Equipment Analyzer is a comprehensive data analysis tool designed for 
            processing and visualizing chemical equipment parameters. Upload CSV files containing 
            equipment data and get instant insights through interactive charts and detailed analytics.
          </p>
        </div>

        <div className="about-card">
          <div className="card-icon">📊</div>
          <h3>Features</h3>
          <ul className="features-list">
            <li>📤 Easy CSV file upload and validation</li>
            <li>📈 Interactive data visualization with charts</li>
            <li>📜 History management (last 5 datasets)</li>
            <li>📄 PDF report generation</li>
            <li>🔐 Secure authentication system</li>
            <li>💻 Available on Web and Desktop</li>
          </ul>
        </div>

        <div className="about-card">
          <div className="card-icon">📋</div>
          <h3>CSV Format</h3>
          <p>Your CSV file must include the following columns:</p>
          <div className="csv-columns">
            <span className="column-badge">Equipment Name</span>
            <span className="column-badge">Type</span>
            <span className="column-badge">Flowrate</span>
            <span className="column-badge">Pressure</span>
            <span className="column-badge">Temperature</span>
          </div>
          <p className="csv-note">
            Column names are case-insensitive. Numeric columns (Flowrate, Pressure, Temperature) 
            should contain valid numbers.
          </p>
        </div>

        <div className="about-card">
          <div className="card-icon">🔧</div>
          <h3>Technology Stack</h3>
          <div className="tech-stack">
            <div className="tech-item">
              <strong>Backend:</strong> Django REST Framework, Pandas, ReportLab
            </div>
            <div className="tech-item">
              <strong>Web Frontend:</strong> React, Chart.js, Axios
            </div>
            <div className="tech-item">
              <strong>Desktop:</strong> PyQt5, Matplotlib
            </div>
            <div className="tech-item">
              <strong>Database:</strong> SQLite
            </div>
          </div>
        </div>

        <div className="about-card">
          <div className="card-icon">💡</div>
          <h3>How to Use</h3>
          <ol className="usage-steps">
            <li>Register or login to your account</li>
            <li>Navigate to the Dashboard</li>
            <li>Upload a CSV file with equipment data</li>
            <li>View interactive visualizations and statistics</li>
            <li>Check your upload history</li>
            <li>Download PDF reports for your analyses</li>
          </ol>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;

