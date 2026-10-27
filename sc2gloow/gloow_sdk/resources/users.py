"""Users resource."""

from typing import Optional, Dict, Any, List, Tuple
from ..models import Track


class Users:
    """Users API resource."""
    
    def __init__(self, http_client):
        self.http = http_client
    
    def get(self, handle: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Get user by handle."""
        response = self.http.get(f"/api/users/{handle}")
        if response.status_code != 200:
            return None, f"Not found: {response.status_code}"
        return response.json(), None
    
    def me(self) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Get current user."""
        response = self.http.get("/api/me")
        if response.status_code != 200:
            return None, f"Failed: {response.status_code}"
        return response.json(), None
    
    def get_tracks(self, handle: str) -> Tuple[List[Track], Optional[str]]:
        """Get user's tracks."""
        user_data, err = self.get(handle)
        if err:
            return [], err
        tracks = [Track.from_dict(t) for t in user_data.get("tracks", [])]
        return tracks, None
