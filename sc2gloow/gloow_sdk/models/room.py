"""Room model."""

from dataclasses import dataclass
from typing import Optional, Dict, Any
from .track import Author


@dataclass
class Room:
    """Room model."""
    id: str
    name: str
    visibility: str
    owner: Author
    listeners: int = 0
    now_playing: Optional[Dict[str, Any]] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Room":
        owner_data = data.get("owner", {})
        owner = Author.from_dict(owner_data)
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            visibility=data.get("visibility", ""),
            owner=owner,
            listeners=data.get("listeners", 0),
            now_playing=data.get("nowPlaying")
        )
