import os
import time
import requests


class GloowroomUploader:
    """Uploads tracks to Gloowroom."""

    def __init__(self, session_token, api_url="https://gloowroom.com", upload_timeout=300, processing_timeout=90):
        self.api_url = api_url
        self.cookies = {"__Secure-better-auth.session_token": session_token}
        self.upload_timeout = upload_timeout
        self.processing_timeout = processing_timeout

    def upload_track(self, audio_path, title, description="", cover_path=None):
        """Upload a single track. Returns track_id or None."""
        # Step 1: Create track
        dummy = b"\x00" * 100
        files = {"file": ("dummy.mp3", dummy, "audio/mpeg")}
        data = {
            "title": title,
            "rights": "true",
            "description": description,
            "explicit": "false",
        }

        r = requests.post(
            f"{self.api_url}/api/tracks",
            cookies=self.cookies,
            files=files,
            data=data,
            timeout=30,
        )

        if r.status_code != 201:
            return None, f"Create failed: {r.status_code}"

        resp = r.json()
        track = resp["track"]
        upload_url = resp["uploadUrl"]
        track_id = track["id"]

        # Step 2: Upload audio
        content_type = self._audio_content_type(audio_path)
        file_size = os.path.getsize(audio_path) / (1024 * 1024)

        with open(audio_path, "rb") as f:
            r2 = requests.put(
                upload_url,
                data=f,
                cookies=self.cookies,
                headers={"Content-Type": content_type},
                timeout=self.upload_timeout,
            )

        if r2.status_code not in (200, 204):
            return None, f"Audio upload failed: {r2.status_code}"

        # Step 3: Upload cover
        if cover_path and os.path.exists(cover_path):
            cover_ct = self._image_content_type(cover_path)
            with open(cover_path, "rb") as f:
                r3 = requests.put(
                    f"{self.api_url}/api/tracks/{track_id}/cover",
                    cookies=self.cookies,
                    files={"file": (os.path.basename(cover_path), f, cover_ct)},
                    timeout=60,
                )
            if r3.status_code != 200:
                pass  # Cover upload failed but track still created

        # Step 4: Wait for processing
        max_attempts = self.processing_timeout // 3
        for i in range(max_attempts):
            time.sleep(3)
            r4 = requests.get(
                f"{self.api_url}/api/tracks/{track_id}",
                cookies=self.cookies,
                timeout=10,
            )
            if r4.status_code == 200:
                final = r4.json()["track"]
                status = final["status"]
                if status in ("ready", "failed"):
                    if status == "ready":
                        return track_id, f"Ready: {self.api_url}/tracks/{final['slug']}"
                    return None, "Processing failed"
        return track_id, "Timeout waiting for processing"

    @staticmethod
    def _audio_content_type(path):
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
    def _image_content_type(path):
        ext_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
        }
        ext = os.path.splitext(path)[1].lower()
        return ext_map.get(ext, "image/jpeg")
