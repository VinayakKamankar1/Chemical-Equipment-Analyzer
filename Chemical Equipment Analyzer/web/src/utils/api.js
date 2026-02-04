import axios from 'axios';
import { getAuthToken } from './auth';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = getAuthToken();
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const register = async (username, password, email = '') => {
  const response = await api.post('/register/', {
    username,
    password,
    email,
  });
  return response.data;
};

export const login = async (username, password) => {
  const response = await api.post('/login/', {
    username,
    password,
  });
  return response.data;
};

export const uploadCSV = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await api.post('/upload/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getHistory = async () => {
  const response = await api.get('/history/');
  return response.data;
};

export const getSummary = async (summaryId) => {
  const response = await api.get(`/summary/${summaryId}/`);
  return response.data;
};

export const downloadPDF = async (summaryId) => {
  const token = getAuthToken();
  const response = await fetch(`${API_BASE_URL}/summary/${summaryId}/pdf/`, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
  
  if (!response.ok) {
    throw new Error('Failed to download PDF');
  }
  
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `report_${summaryId}.pdf`;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
};

