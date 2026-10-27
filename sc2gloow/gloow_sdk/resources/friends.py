"""Friends resource."""

from typing import Optional, List, Dict, Any, Tuple


class Friends:
    """Friends API resource."""
    
    def __init__(self, http_client):
        self.http = http_client
    
    def list(self) -> Tuple[Dict[str, Any], Optional[str]]:
        """List friends."""
        response = self.http.get("/api/friends")
        if response.status_code != 200:
            return {}, f"Failed: {response.status_code}"
        return response.json(), None
    
    def get_requests(self) -> Tuple[Dict[str, Any], Optional[str]]:
        """Get friend requests."""
        response = self.http.get("/api/friends/requests")
        if response.status_code == 404:
            return {"incoming": [], "outgoing": []}, None
        if response.status_code != 200:
            return {}, f"Failed: {response.status_code}"
        return response.json(), None
