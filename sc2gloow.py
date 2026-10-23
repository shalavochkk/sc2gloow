#!/usr/bin/env python3
"""
sc2gloow - SoundCloud to Gloowroom transfer tool

Downloads tracks from SoundCloud and uploads them to Gloowroom.

Usage:
    python sc2gloow.py <soundcloud_url>
    python sc2gloow.py <soundcloud_url> --config config/config.json
"""

import argparse
import os
import shutil
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sc2gloow.core.downloader import SoundCloudDownloader
from sc2gloow.core.uploader import GloowroomUploader
from sc2gloow.utils.config import load_config


def main():
    parser = argparse.ArgumentParser(
        description="Transfer tracks from SoundCloud to Gloowroom"
    )
    parser.add_argument("url", help="SoundCloud track or playlist URL")
    parser.add_argument(
        "--config", default="config/config.json", help="Path to config file"
    )
    parser.add_argument(
        "--output-dir", default=None, help="Output directory for downloads"
    )
    args = parser.parse_args()

    # Load config
    config = load_config(args.config)
    session_token = config.get("gloowroom_session_token", "")
    if session_token == "YOUR_GLOOWROOM_SESSION_TOKEN" or not session_token:
        print("ERROR: Set your Gloowroom session token in config/config.json")
        sys.exit(1)

    output_dir = args.output_dir or config.get("output_dir", "./downloads")
    os.makedirs(output_dir, exist_ok=True)

    # Initialize
    downloader = SoundCloudDownloader(output_dir=output_dir)
    uploader = GloowroomUploader(
        session_token=session_token,
        api_url=config.get("gloowroom_api_url", "https://gloowroom.com"),
        upload_timeout=config.get("upload_timeout", 300),
        processing_timeout=config.get("processing_timeout", 90),
    )

    # Extract track list
    tracks, album_title = downloader.extract_track_list(args.url)
    print(f"\n{'='*50}")
    print(f"Found {len(tracks)} track(s) to transfer")
    if album_title:
        print(f"Album: {album_title}")
    print(f"{'='*50}\n")

    results = []
    for i, track in enumerate(tracks, 1):
        print(f"\n{'='*50}")
        print(f"[{i}/{len(tracks)}] {track.get('title', 'Untitled')}")
        print(f"{'='*50}")

        track_url = track.get("url", "")
        if not track_url:
            print("    No URL, skipping")
            results.append((track.get("title", "Unknown"), False))
            continue

        work_dir = None
        try:
            audio_path, cover_path, title, description, work_dir = downloader.download(track_url)

            if not audio_path:
                print("    No audio file, skipping upload")
                results.append((title, False))
                continue

            track_id, msg = uploader.upload_track(audio_path, title, description, cover_path)
            print(f"    {msg}")
            results.append((title, track_id is not None))
        except Exception as e:
            print(f"    ERROR: {e}")
            results.append((track.get("title", "Unknown"), False))
        finally:
            if work_dir and os.path.exists(work_dir):
                try:
                    shutil.rmtree(work_dir)
                except Exception:
                    pass

    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    success = sum(1 for _, ok in results if ok)
    print(f"Uploaded: {success}/{len(results)}")
    for title, ok in results:
        print(f"  {'OK' if ok else 'FAIL'} {title}")


if __name__ == "__main__":
    main()
