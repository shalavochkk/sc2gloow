import os
import re
import tempfile
import shutil
import yt_dlp


class SoundCloudDownloader:
    """Downloads tracks from SoundCloud using yt-dlp."""

    def __init__(self, output_dir=None):
        self.output_dir = output_dir or tempfile.mkdtemp(prefix="sc_dl_")

    def extract_track_list(self, sc_url):
        """Extract track list from URL (single track or playlist)."""
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": True,
            "legacy_server_connect": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(sc_url, download=False)

        if info.get("_type") == "playlist":
            entries = info.get("entries", [])
            tracks = []
            for e in entries:
                url = e.get("url") or e.get("webpage_url") or ""
                if not url and e.get("id"):
                    url = f"https://soundcloud.com/{e.get('uploader', '')}/{e.get('id', '')}"
                tracks.append({
                    "title": e.get("title", "Untitled"),
                    "url": url,
                })
            return tracks, info.get("title", "Album")
        else:
            return [{"title": info.get("title", "Untitled"), "url": sc_url}], None

    def download(self, sc_url):
        """Download a single track. Returns (audio_path, cover_path, title, description)."""
        work_dir = tempfile.mkdtemp(prefix="sc_dl_", dir=self.output_dir)
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(work_dir, "%(title)s.%(ext)s"),
            "writethumbnail": True,
            "quiet": True,
            "no_warnings": True,
            "legacy_server_connect": True,
            "fixup": "never",
            "postprocessors": [],
        }
        info = None
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(sc_url, download=True)
        except Exception:
            pass

        title = "Untitled"
        description = ""
        if info:
            title = info.get("title", "Untitled")
            description = info.get("description", "") or ""
            description = re.sub(r"<[^>]+>", "", description).strip()[:500]

        # Find downloaded files
        audio_path = None
        cover_path = None
        for f in os.listdir(work_dir):
            full = os.path.join(work_dir, f)
            if not os.path.isfile(full):
                continue
            if f.endswith((".m4a", ".mp3", ".webm", ".opus", ".ogg", ".aac", ".wav", ".flac")):
                audio_path = full
            elif f.endswith((".jpg", ".jpeg", ".png", ".webp")):
                cover_path = full

        return audio_path, cover_path, title, description, work_dir
