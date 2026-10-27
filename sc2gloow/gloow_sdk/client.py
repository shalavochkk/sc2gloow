"""Main GloowClient."""

from typing import Optional
from .utils.http import HTTPClient
from .auth import Auth
from .resources import Tracks, Users, Rooms, Friends, Notifications


class GloowClient:
    """
    Main client for Gloowroom API.
    
    Usage:
        client = GloowClient(session_token="your_token")
        me = client.me()
        tracks, err = client.tracks.list()
    """
    
    def __init__(self, session_token: Optional[str] = None, 
                 base_url: str = "https://gloowroom.com",
                 timeout: int = 30):
        self.http = HTTPClient(base_url=base_url, session_token=session_token, timeout=timeout)
        self.auth = Auth(self.http)
        self.tracks = Tracks(self.http)
        self.users = Users(self.http)
        self.rooms = Rooms(self.http)
        self.friends = Friends(self.http)
        self.notifications = Notifications(self.http)
    
    def me(self):
        """Get current user info."""
        return self.users.me()
    
    def get_session(self):
        """Get current session."""
        return self.auth.get_session()
    
    def is_authenticated(self):
        """Check authentication status."""
        return self.auth.is_authenticated()
    
    def set_session_token(self, token: str):
        """Update session token."""
        self.http.set_session_token(token)
