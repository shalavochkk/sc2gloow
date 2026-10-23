"""Gloowroom SDK — Python client for Gloowroom API."""

import os
import time
import requests


class GloowroomClient:
    """Client for interacting with the Gloowroom API."""

    def __init__(self, session_token, base_url="https://gloowroom.com", timeout=30):
        self.base_url = base_url.rstrip("/")
        self.session_token = session_token
        self.timeout = timeout
        self.cookies = {"__Secure-better-auth.session_token": session_token}

    def _request(self, method, path, **kwargs):
        """Make an authenticated request to the Gloowroom API."""
        url = f"{self.base_url}{path}"
        kwargs.setdefault("cookies", self.cookies)
        kwargs.setdefault("timeout", self.timeout)
        return requests.request(method, url, **kwargs)

    # --- Tracks ---

    def create_track(self, title, audio_path, description="", genre=None, explicit=False):
        """
        Create a new track entry.

        Returns (track_id, upload_url) on success, (None, error) on failure.
        """
        dummy = b"\x00" * 100
        files = {"file": ("dummy.mp3", dummy, "audio/mpeg")}
        data = {
            "title": title,
            "rights": "true",
            "description": description,
            "explicit": "true" if explicit else "false",
        }
        if genre:
            data["genre"] = genre

        r = self._request("POST", "/api/tracks", files=files, data=data)
        if r.status_code != 201:
            return None, None, f"Create failed: {r.status_code} — {r.text[:200]}"

        resp = r.json()
        track = resp["track"]
        return track["id"], resp["uploadUrl"], None

    def upload_audio(self, upload_url, audio_path, content_type=None):
        """Upload audio bytes to the provided upload URL."""
        if content_type is None:
            content_type = self._guess_audio_type(audio_path)

        with open(audio_path, "rb") as f:
            r = requests.put(
                upload_url,
                data=f,
                cookies=self.cookies,
                headers={"Content-Type": content_type},
                timeout=300,
            )
        if r.status_code not in (200, 204):
            return False, f"Upload failed: {r.status_code} — {r.text[:200]}"
        return True, "OK"

    def upload_cover(self, track_id, cover_path):
        """Upload cover art for a track."""
        content_type = self._guess_image_type(cover_path)
        with open(cover_path, "rb") as f:
            r = self._request(
                "PUT",
                f"/api/tracks/{track_id}/cover",
                files={"file": (os.path.basename(cover_path), f, content_type)},
                timeout=60,
            )
        if r.status_code != 200:
            return False, f"Cover upload failed: {r.status_code}"
        return True, "OK"

    def get_track(self, track_id):
        """Get track details."""
        r = self._request("GET", f"/api/tracks/{track_id}")
        if r.status_code != 200:
            return None, f"Not found: {r.status_code}"
        return r.json().get("track"), None

    def wait_for_processing(self, track_id, timeout=90, poll_interval=3):
        """Wait for track to finish processing."""
        max_attempts = timeout // poll_interval
        for i in range(max_attempts):
            time.sleep(poll_interval)
            track, err = self.get_track(track_id)
            if track:
                status = track.get("status", "")
                if status in ("ready", "failed"):
                    if status == "ready":
                        return track, None
                    return track, "Processing failed"
        return None, "Timeout waiting for processing"

    def upload_track_full(self, audio_path, title, description="", cover_path=None, genre=None, explicit=False):
        """
        Full upload flow: create + upload audio + cover + wait for processing.

        Returns (track_id, track_url, error).
        """
        # Create
        track_id, upload_url, err = self.create_track(title, audio_path, description, genre, explicit)
        if err:
            return None, None, err

        # Upload audio
        ok, msg = self.upload_audio(upload_url, audio_path)
        if not ok:
            return track_id, None, msg

        # Upload cover
        if cover_path and os.path.exists(cover_path):
            ok, msg = self.upload_cover(track_id, cover_path)
            if not ok:
                pass  # Non-critical

        # Wait for processing
        track, err = self.wait_for_processing(track_id)
        if err:
            return track_id, None, err

        track_url = f"{self.base_url}/tracks/{track['slug']}"
        return track_id, track_url, None

    def list_tracks(self, limit=20, offset=0):
        """List tracks."""
        r = self._request("GET", f"/api/tracks?limit={limit}&offset={offset}")
        if r.status_code != 200:
            return [], f"Failed: {r.status_code}"
        return r.json().get("tracks", []), None

    def delete_track(self, track_id):
        """Delete a track."""
        r = self._request("DELETE", f"/api/tracks/{track_id}")
        return r.status_code in (200, 204), r.text[:200]

    @staticmethod
    def _guess_audio_type(path):
        ext_map = {
            ".m4a": "audio/mp4",
            ".mp3": "audio/mpeg",
            ".ogg": "audio/ogg",
            ".wav": "audio/wav",
            ".flac": "audio/flac",
            ".aac": "audio/aac",
            ".webm": "audio/webm",
        }
        ext = os.path.splitext(path)[1].lower()
        return ext_map.get(ext, "audio/mpeg")

    @staticmethod
    def _guess_image_type(path):
        ext_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        ext = os.path.splitext(path)[1].lower()
        return ext_map.get(ext, "image/jpeg")
