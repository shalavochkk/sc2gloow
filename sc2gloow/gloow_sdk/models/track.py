"""Track model."""

from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass
class Author:
    """Track author model."""
    id: str
    handle: str
    name: str
    image: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Author":
        return cls(
            id=data.get("id", ""),
            handle=data.get("handle", ""),
            name=data.get("name", ""),
            image=data.get("image")
        )


@dataclass
class Track:
    """Track model."""
    id: str
    title: str
    slug: str
    author: Author
    duration_ms: int
    status: str
    audio_url: str
    cover_url: Optional[str] = None
    description: str = ""
    genre: Optional[str] = None
    waveform: Optional[List[int]] = None
    plays: int = 0
    likes: int = 0
    liked: bool = False
    favorited: bool = False
    disliked: bool = False
    reposts: int = 0
    reposted: bool = False
    has_lyrics: bool = False
    explicit: bool = False
    gain_db: Optional[float] = None
    created_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Track":
        author_data = data.get("author", {})
        author = Author.from_dict(author_data) if author_data else Author("", "", "")
        
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            slug=data.get("slug", ""),
            author=author,
            duration_ms=data.get("durationMs", 0),
            status=data.get("status", ""),
            audio_url=data.get("audioUrl", ""),
            cover_url=data.get("coverUrl"),
            description=data.get("description", ""),
            genre=data.get("genre"),
            waveform=data.get("waveform"),
            plays=data.get("plays", 0),
            likes=data.get("likes", 0),
            liked=data.get("liked", False),
            favorited=data.get("favorited", False),
            disliked=data.get("disliked", False),
            reposts=data.get("reposts", 0),
            reposted=data.get("reposted", False),
            has_lyrics=data.get("hasLyrics", False),
            explicit=data.get("explicit", False),
            gain_db=data.get("gainDb"),
            created_at=data.get("createdAt")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "author": {
                "id": self.author.id,
                "handle": self.author.handle,
                "name": self.author.name,
                "image": self.author.image
            },
            "durationMs": self.duration_ms,
            "status": self.status,
            "audioUrl": self.audio_url,
            "coverUrl": self.cover_url,
            "description": self.description,
            "genre": self.genre,
            "waveform": self.waveform,
            "plays": self.plays,
            "likes": self.likes,
            "liked": self.liked,
            "favorited": self.favorited,
            "disliked": self.disliked,
            "reposts": self.reposts,
            "reposted": self.reposted,
            "hasLyrics": self.has_lyrics,
            "explicit": self.explicit,
            "gainDb": self.gain_db,
            "createdAt": self.created_at
        }
