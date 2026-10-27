#!/usr/bin/env python3
"""
sc2gloow — SoundCloud to Gloowroom transfer tool

Downloads tracks from SoundCloud and uploads them to Gloowroom.
Uses gloow_sdk for Gloowroom API interaction.

Usage:
    python sc2gloow.py <soundcloud_url>
    python sc2gloow.py <soundcloud_url> --config config/config.json
"""

import argparse
import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sc2gloow.sdk.soundcloud import SoundCloudDownloader
from gloow_sdk import GloowClient
from sc2gloow.utils.config import load_config


def main():
    parser = argparse.ArgumentParser(
        description="Transfer tracks from SoundCloud to Gloowroom"
    )
    parser.add_argument("url", help="SoundCloud track or playlist URL")
    parser.add_argument("--config", default="config/config.json", help="Config path")
    parser.add_argument("--output-dir", default=None, help="Output directory")
    args = parser.parse_args()

    config = load_config(args.config)
    session_token = config.get("gloowroom_session_token", "")
    if not session_token or "YOUR_" in session_token:
        print("ERROR: Set gloowroom_session_token in config/config.json")
        sys.exit(1)

    output_dir = args.output_dir or config.get("output_dir", "./downloads")
    os.makedirs(output_dir, exist_ok=True)

    downloader = SoundCloudDownloader(output_dir=output_dir)
    client = GloowClient(session_token=session_token)

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

        work_dir = tempfile.mkdtemp(prefix="sc_dl_")
        try:
            audio_path, cover_path, title, description = downloader.download(track_url, work_dir)

            if not audio_path:
                print("    No audio file, skipping")
                results.append((title, False))
                continue

            track_obj, err = client.tracks.upload(
                audio_path=audio_path,
                title=title,
                description=description,
                cover_path=cover_path,
            )
            if err:
                print(f"    {err}")
                results.append((title, False))
            else:
                print(f"    Uploaded: https://gloowroom.com/tracks/{track_obj.slug}")
                results.append((title, True))
        except Exception as e:
            print(f"    ERROR: {e}")
            results.append((track.get("title", "Unknown"), False))
        finally:
            if os.path.exists(work_dir):
                try:
                    shutil.rmtree(work_dir)
                except Exception:
                    pass

    print(f"\n{'='*50}")
    print("SUMMARY")
    print(f"{'='*50}")
    success = sum(1 for _, ok in results if ok)
    print(f"Uploaded: {success}/{len(results)}")
    for title, ok in results:
        print(f"  {'OK' if ok else 'FAIL'} {title}")


if __name__ == "__main__":
    main()
