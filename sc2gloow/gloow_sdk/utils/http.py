"""HTTP client utilities."""

import json
from typing import Any, Dict, Optional
import requests


class HTTPClient:
    """Low-level HTTP client for Gloowroom API."""
    
    def __init__(self, base_url: str = "https://gloowroom.com", 
                 session_token: Optional[str] = None,
                 timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        if session_token:
            self.set_session_token(session_token)
    
    def set_session_token(self, token: str):
        """Set session token cookie."""
        self.session.cookies.set(
            "__Secure-better-auth.session_token",
            token,
            domain="gloowroom.com",
            secure=True,
            rest={'HttpOnly': True}
        )
    
    def request(self, method: str, path: str, 
                params: Optional[Dict] = None,
                data: Optional[Dict] = None,
                json_data: Optional[Dict] = None,
                files: Optional[Dict] = None,
                headers: Optional[Dict] = None,
                **kwargs) -> requests.Response:
        """Make HTTP request."""
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", self.timeout)
        
        if json_data is not None:
            headers = headers or {}
            headers.setdefault("Content-Type", "application/json")
            response = self.session.request(
                method, url, params=params, json=json_data,
                headers=headers, **kwargs
            )
        elif files is not None:
            response = self.session.request(
                method, url, params=params, data=data,
                files=files, headers=headers, **kwargs
            )
        else:
            response = self.session.request(
                method, url, params=params, data=data,
                headers=headers, **kwargs
            )
        return response
    
    def get(self, path: str, **kwargs) -> requests.Response:
        return self.request("GET", path, **kwargs)
    
    def post(self, path: str, **kwargs) -> requests.Response:
        return self.request("POST", path, **kwargs)
    
    def put(self, path: str, **kwargs) -> requests.Response:
        return self.request("PUT", path, **kwargs)
    
    def patch(self, path: str, **kwargs) -> requests.Response:
        return self.request("PATCH", path, **kwargs)
    
    def delete(self, path: str, **kwargs) -> requests.Response:
        return self.request("DELETE", path, **kwargs)
