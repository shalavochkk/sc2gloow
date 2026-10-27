"""Rooms resource."""

from typing import Optional, List, Dict, Any, Tuple
from ..models import Room


class Rooms:
    """Rooms API resource."""
    
    def __init__(self, http_client):
        self.http = http_client
    
    def list(self) -> Tuple[List[Room], Optional[str]]:
        """List all rooms."""
        response = self.http.get("/api/rooms")
        if response.status_code != 200:
            return [], f"Failed: {response.status_code}"
        data = response.json()
        rooms = [Room.from_dict(r) for r in data.get("rooms", [])]
        return rooms, None
    
    def get(self, room_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """Get room details."""
        response = self.http.get(f"/api/rooms/{room_id}")
        if response.status_code != 200:
            return None, f"Not found: {response.status_code}"
        return response.json(), None
