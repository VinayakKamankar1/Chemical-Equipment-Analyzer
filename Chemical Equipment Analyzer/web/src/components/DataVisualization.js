import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import { downloadPDF } from '../utils/api';
import './DataVisualization.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const DataVisualization = ({ data }) => {
  const handleDownloadPDF = async () => {
    try {
      await downloadPDF(data.id);
    } catch (error) {
      alert('Failed to download PDF');
    }
  };

  // Prepare data for charts
  const averagesData = {
    labels: ['Flowrate', 'Pressure', 'Temperature'],
    datasets: [
      {
        label: 'Average Values',
        data: [
          data.avg_flowrate,
          data.avg_pressure,
          data.avg_temperature,
        ],
        backgroundColor: [
          'rgba(16, 185, 129, 0.8)',
          'rgba(5, 150, 105, 0.8)',
          'rgba(107, 114, 128, 0.8)',
        ],
      },
    ],
  };

  const typeDistribution = data.equipment_type_distribution || {};
  const typeLabels = Object.keys(typeDistribution);
  const typeValues = Object.values(typeDistribution);

  const typeDistributionData = {
    labels: typeLabels,
    datasets: [
      {
        data: typeValues,
        backgroundColor: [
          'rgba(16, 185, 129, 0.8)',
          'rgba(5, 150, 105, 0.8)',
          'rgba(107, 114, 128, 0.8)',
          'rgba(75, 85, 99, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(6, 182, 212, 0.8)',
        ],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
    },
  };

  return (
    <div>
      <div className="card">
        <div className="visualization-header">
          <h2>Analysis Results: {data.filename}</h2>
          <button onClick={handleDownloadPDF} className="btn btn-secondary">
            Download PDF Report
          </button>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <h3>{data.total_equipment_count}</h3>
            <p>Total Equipment</p>
          </div>
          <div className="stat-card">
            <h3>{data.avg_flowrate.toFixed(2)}</h3>
            <p>Avg Flowrate</p>
          </div>
          <div className="stat-card">
            <h3>{data.avg_pressure.toFixed(2)}</h3>
            <p>Avg Pressure</p>
          </div>
          <div className="stat-card">
            <h3>{data.avg_temperature.toFixed(2)}</h3>
            <p>Avg Temperature</p>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>Average Values</h2>
        <div className="chart-container">
          <Bar data={averagesData} options={chartOptions} />
        </div>
      </div>

      {typeLabels.length > 0 && (
        <div className="card">
          <h2>Equipment Type Distribution</h2>
          <div className="chart-container">
            <Pie data={typeDistributionData} options={chartOptions} />
          </div>
        </div>
      )}

      {data.raw_data && data.raw_data.length > 0 && (
        <div className="card">
          <h2>Data Table (First 100 rows)</h2>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Equipment Name</th>
                  <th>Type</th>
                  <th>Flowrate</th>
                  <th>Pressure</th>
                  <th>Temperature</th>
                </tr>
              </thead>
              <tbody>
                {data.raw_data.map((row, index) => (
                  <tr key={index}>
                    <td>{row['Equipment Name']}</td>
                    <td>{row['Type']}</td>
                    <td>{row['Flowrate']}</td>
                    <td>{row['Pressure']}</td>
                    <td>{row['Temperature']}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataVisualization;

