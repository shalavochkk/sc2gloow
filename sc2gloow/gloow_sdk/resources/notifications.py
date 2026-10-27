"""Notifications resource."""

from typing import Optional, List, Dict, Any, Tuple


class Notifications:
    """Notifications API resource."""
    
    def __init__(self, http_client):
        self.http = http_client
    
    def list(self) -> Tuple[List[Dict[str, Any]], Optional[str]]:
        """List notifications."""
        response = self.http.get("/api/notifications")
        if response.status_code != 200:
            return [], f"Failed: {response.status_code}"
        data = response.json()
        return data.get("notifications", []), None
