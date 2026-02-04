import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Layout.css';

const Layout = ({ children, onLogout }) => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path ? 'active' : '';
  };

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <div className="nav-brand">
            <div className="brand-icon">⚗️</div>
            <h1>Chemical Equipment Analyzer</h1>
          </div>
          <div className="nav-links">
            <Link to="/dashboard" className={`nav-link ${isActive('/dashboard')}`}>
              <span className="nav-icon">📊</span>
              Dashboard
            </Link>
            <Link to="/history" className={`nav-link ${isActive('/history')}`}>
              <span className="nav-icon">📜</span>
              History
            </Link>
            <Link to="/about" className={`nav-link ${isActive('/about')}`}>
              <span className="nav-icon">ℹ️</span>
              About
            </Link>
            <button onClick={onLogout} className="nav-link logout-btn">
              <span className="nav-icon">🚪</span>
              Logout
            </button>
          </div>
        </div>
      </nav>
      <main className="main-content">
        <div className="content-wrapper">
          {children}
        </div>
      </main>
    </div>
  );
};

export default Layout;

