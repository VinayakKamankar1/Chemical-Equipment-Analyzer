import React, { useState } from 'react';
import { uploadCSV } from '../utils/api';
import './CSVUpload.css';

const CSVUpload = ({ onUploadSuccess }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.name.endsWith('.csv')) {
        setFile(selectedFile);
        setError('');
      } else {
        setError('Please select a CSV file');
        setFile(null);
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await uploadCSV(file);
      onUploadSuccess(data);
      setFile(null);
      // Reset file input
      e.target.reset();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload file');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h2>Upload CSV File</h2>
      <p className="upload-info">
        Upload a CSV file containing columns: Equipment Name, Type, Flowrate, Pressure, Temperature
      </p>

      {error && <div className="alert alert-error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="file-upload">
          <input
            type="file"
            id="csv-file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={loading}
          />
          <label htmlFor="csv-file" className="file-upload-label">
            {file ? file.name : 'Choose CSV File'}
          </label>
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          disabled={!file || loading}
        >
          {loading ? 'Uploading...' : 'Upload & Analyze'}
        </button>
      </form>
    </div>
  );
};

export default CSVUpload;

