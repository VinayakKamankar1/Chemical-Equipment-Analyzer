import requests
import os
from typing import Optional, Dict, List

API_BASE_URL = 'http://localhost:8000/api'


class APIClient:
    def __init__(self):
        self.token: Optional[str] = None
        self.base_url = API_BASE_URL
    
    def set_token(self, token: str):
        """Set authentication token"""
        self.token = token
    
    def _get_headers(self) -> Dict:
        """Get headers with authentication"""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Token {self.token}'
        return headers
    
    def register(self, username: str, password: str, email: str = '') -> Dict:
        """Register a new user"""
        response = requests.post(
            f'{self.base_url}/register/',
            json={'username': username, 'password': password, 'email': email}
        )
        if response.status_code == 201:
            data = response.json()
            self.token = data.get('token')
            return data
        else:
            raise Exception(response.json().get('error', 'Registration failed'))
    
    def login(self, username: str, password: str) -> Dict:
        """Login and get token"""
        response = requests.post(
            f'{self.base_url}/login/',
            json={'username': username, 'password': password}
        )
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('token')
            return data
        else:
            raise Exception(response.json().get('error', 'Login failed'))
    
    def upload_csv(self, file_path: str) -> Dict:
        """Upload CSV file"""
        if not self.token:
            raise Exception('Not authenticated')
        
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.post(
                f'{self.base_url}/upload/',
                files=files,
                headers=headers
            )
        
        if response.status_code == 201:
            return response.json()
        else:
            raise Exception(response.json().get('error', 'Upload failed'))
    
    def get_history(self) -> List[Dict]:
        """Get upload history"""
        if not self.token:
            raise Exception('Not authenticated')
        
        response = requests.get(
            f'{self.base_url}/history/',
            headers=self._get_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to fetch history')
    
    def get_summary(self, summary_id: int) -> Dict:
        """Get dataset summary"""
        if not self.token:
            raise Exception('Not authenticated')
        
        response = requests.get(
            f'{self.base_url}/summary/{summary_id}/',
            headers=self._get_headers()
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('Failed to fetch summary')
    
    def download_pdf(self, summary_id: int, save_path: str):
        """Download PDF report"""
        if not self.token:
            raise Exception('Not authenticated')
        
        headers = {'Authorization': f'Token {self.token}'}
        response = requests.get(
            f'{self.base_url}/summary/{summary_id}/pdf/',
            headers=headers,
            stream=True
        )
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        else:
            raise Exception('Failed to download PDF')

