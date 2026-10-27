"""User model."""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class User:
    """User model."""
    id: str
    handle: str
    name: str
    email: Optional[str] = None
    image: Optional[str] = None
    email_verified: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "User":
        return cls(
            id=data.get("id", ""),
            handle=data.get("handle", ""),
            name=data.get("name", ""),
            email=data.get("email"),
            image=data.get("image"),
            email_verified=data.get("emailVerified", False),
            created_at=data.get("createdAt"),
            updated_at=data.get("updatedAt")
        )
