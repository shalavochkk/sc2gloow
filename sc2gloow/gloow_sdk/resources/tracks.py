"""Tracks resource."""

import os
import time
from typing import Optional, List, Dict, Any, Tuple
from ..models import Track


class Tracks:
    """Tracks API resource."""
    
    def __init__(self, http_client):
        self.http = http_client
    
    def list(self, limit: int = 20, offset: int = 0) -> Tuple[List[Track], Optional[str]]:
        """List tracks."""
        response = self.http.get(f"/api/tracks?limit={limit}&offset={offset}")
        if response.status_code != 200:
            return [], f"Failed: {response.status_code}"
        data = response.json()
        tracks = [Track.from_dict(t) for t in data.get("tracks", [])]
        return tracks, None
    
    def get(self, track_id: str) -> Tuple[Optional[Track], Optional[str]]:
        """Get track by ID."""
        response = self.http.get(f"/api/tracks/{track_id}")
        if response.status_code != 200:
            return None, f"Not found: {response.status_code}"
        data = response.json()
        return Track.from_dict(data.get("track", {})), None
    
    def create(self, title: str, description: str = "", genre: Optional[str] = None, 
               explicit: bool = False) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Create track entry. Returns (track_id, upload_url, error)"""
        dummy = b"\x00" * 100
        files = {"file": ("dummy.mp3", dummy, "audio/mpeg")}
        data = {"title": title, "rights": "true", "description": description, "explicit": "true" if explicit else "false"}
        if genre:
            data["genre"] = genre
        response = self.http.post("/api/tracks", files=files, data=data)
        if response.status_code != 201:
            return None, None, f"Create failed: {response.status_code}"
        resp = response.json()
        track = resp["track"]
        return track["id"], resp["uploadUrl"], None
    
    def upload_audio(self, upload_url: str, audio_path: str, content_type: Optional[str] = None) -> Tuple[bool, str]:
        if content_type is None:
            content_type = self._guess_audio_type(audio_path)
        with open(audio_path, "rb") as f:
            response = self.http.session.put(upload_url, data=f, headers={"Content-Type": content_type}, timeout=300)
        if response.status_code not in (200, 204):
            return False, f"Upload failed: {response.status_code}"
        return True, "OK"
    
    def upload_cover(self, track_id: str, cover_path: str) -> Tuple[bool, str]:
        content_type = self._guess_image_type(cover_path)
        with open(cover_path, "rb") as f:
            response = self.http.put(f"/api/tracks/{track_id}/cover", files={"file": (os.path.basename(cover_path), f, content_type)}, timeout=60)
        if response.status_code != 200:
            return False, f"Cover upload failed: {response.status_code}"
        return True, "OK"
    
    def upload(self, audio_path: str, title: str, description: str = "",
               cover_path: Optional[str] = None, genre: Optional[str] = None,
               explicit: bool = False, wait_for_processing: bool = True,
               processing_timeout: int = 90) -> Tuple[Optional[Track], Optional[str]]:
        track_id, upload_url, err = self.create(title, description, genre, explicit)
        if err:
            return None, err
        ok, msg = self.upload_audio(upload_url, audio_path)
        if not ok:
            return None, msg
        if cover_path and os.path.exists(cover_path):
            self.upload_cover(track_id, cover_path)
        if not wait_for_processing:
            track, err = self.get(track_id)
            return track, err
        track, err = self.wait_for_processing(track_id, processing_timeout)
        return track, err
    
    def wait_for_processing(self, track_id: str, timeout: int = 90, poll_interval: int = 3) -> Tuple[Optional[Track], Optional[str]]:
        max_attempts = timeout // poll_interval
        for i in range(max_attempts):
            time.sleep(poll_interval)
            track, err = self.get(track_id)
            if track:
                if track.status == "ready":
                    return track, None
                elif track.status == "failed":
                    return track, "Processing failed"
        return None, "Timeout waiting for processing"
    
    def delete(self, track_id: str) -> Tuple[bool, str]:
        response = self.http.delete(f"/api/tracks/{track_id}")
        if response.status_code in (200, 204):
            return True, "Deleted"
        return False, f"Failed: {response.status_code}"
    
    @staticmethod
    def _guess_audio_type(path: str) -> str:
        ext_map = {".m4a": "audio/mp4", ".mp3": "audio/mpeg", ".ogg": "audio/ogg", ".wav": "audio/wav", ".flac": "audio/flac", ".aac": "audio/aac", ".webm": "audio/webm"}
        ext = os.path.splitext(path)[1].lower()
        return ext_map.get(ext, "audio/mpeg")
    
    @staticmethod
    def _guess_image_type(path: str) -> str:
        ext_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
        ext = o
