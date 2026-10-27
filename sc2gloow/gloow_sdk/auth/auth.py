"""Authentication management."""

from typing import Optional, Dict, Any


class Auth:
    """Authentication handler for Gloowroom."""
    
    def __init__(self, http_client):
        self.http = http_client
    
    def get_session(self) -> Optional[Dict[str, Any]]:
        """Get current session information."""
        response = self.http.get("/api/auth/get-session")
        if response.status_code == 200:
            return response.json()
        return None
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current authenticated user."""
        response = self.http.get("/api/me")
        if response.status_code == 200:
            return response.json()
        return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        session = self.get_session()
        return session is not None and session.get("user") is not None
