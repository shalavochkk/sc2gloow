# sc2gloow

SoundCloud to Gloowroom transfer tool. Downloads tracks (with cover art) from SoundCloud and uploads them to [Gloowroom](https://gloowroom.com).

## Features

- Single track download & upload
- Full playlist/album transfer
- Cover art download and upload
- M4A/MP3/WAV/FLAC/OGG support
- Automatic retry and error handling
- Progress tracking with summary

## Project Structure

```
sc2gloow/
├── sc2gloow.py              # Main entry point
├── config/
│   └── config.json          # Your tokens (gitignored)
├── sc2gloow/
│   ├── core/
│   │   ├── downloader.py    # SoundCloud download logic
│   │   └── uploader.py      # Gloowroom upload logic
│   └── utils/
│       └── config.py        # Config loader
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/yourname/sc2gloow.git
   cd sc2gloow
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install ffmpeg (required by yt-dlp):
   - Windows: `winget install ffmpeg` or download from https://ffmpeg.org
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

4. Configure:
   ```bash
   cp config/config.example.json config/config.json
   ```
   Edit `config/config.json` and fill in your tokens:
   - **Gloowroom session token**: Log in to gloowroom.com, open DevTools (F12) → Application → Cookies → copy `__Secure-better-auth.session_token`
   - **SoundCloud OAuth token**: (optional, yt-dlp works without it for public tracks)

## Usage

### Single track
```bash
python sc2gloow.py https://soundcloud.com/artist/track-name
```

### Playlist / Album
```bash
python sc2gloow.py https://soundcloud.com/artist/sets/album-name
```

### Custom config
```bash
python sc2gloow.py https://soundcloud.com/artist/track --config my_config.json
```

### Custom output directory
```bash
python sc2gloow.py https://soundcloud.com/artist/track --output-dir /tmp/downloads
```

## Getting Tokens

### Gloowroom Session Token
1. Go to [gloowroom.com](https://gloowroom.com) and log in
2. Open DevTools (F12) → Application → Cookies
3. Find `__Secure-better-auth.session_token` and copy its value

### SoundCloud (optional)
Most public tracks work without a token. For private/restricted tracks, you may need an OAuth token.

## How It Works

1. **Extract** — Uses yt-dlp to get track metadata and download URLs
2. **Download** — Downloads audio (M4A/MP3) + cover art to a temp directory
3. **Create** — Creates a track entry on Gloowroom via `POST /api/tracks`
4. **Upload Audio** — Uploads the audio file via `PUT` to the provided upload URL
5. **Upload Cover** — Uploads cover art via `PUT /api/tracks/{id}/cover`
6. **Process** — Waits for Gloowroom to process the track (status: ready)

## Requirements

- Python 3.8+
- ffmpeg
- requests
- yt-dlp

## License

MIT
