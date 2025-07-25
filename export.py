import subprocess
import os
import argparse
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
COOKIES_FILE = BASE_DIR / "cookies.txt"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = OUTPUT_DIR / "data"
AUDIO_DIR = OUTPUT_DIR / "audio"
VIDEO_DIR = OUTPUT_DIR / "video"
DATA_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)

# URLs
LIKED_PLAYLIST_URL = "https://www.youtube.com/playlist?list=LL"

# TXT output
IDS_FILE = DATA_DIR / "liked_ids.txt"
URLS_FILE = DATA_DIR / "liked_urls.txt"

# Parse flags
parser = argparse.ArgumentParser(description="Download your liked YouTube videos or MP3s")
parser.add_argument("--mp3", action="store_true", help="Download audio only in MP3 format")
args = parser.parse_args()

# Determine mode
if args.mp3:
    MODE = "audio"
    TARGET_DIR = AUDIO_DIR
    ARCHIVE_FILE = DATA_DIR / "downloaded_audio.txt"
else:
    MODE = "video"
    TARGET_DIR = VIDEO_DIR
    ARCHIVE_FILE = DATA_DIR / "downloaded_video.txt"

if not COOKIES_FILE.is_file():
    print("❌ cookies.txt not found. Please place it in the script folder.")
    exit(1)

# Warn if archive file doesn't exist
if not ARCHIVE_FILE.is_file():
    print(f"⚠️ Archive file not found for {MODE}. This may re-download all your liked {MODE}.")

print("📥 Extracting video IDs from your liked playlist...")
with open(IDS_FILE, "w") as id_file:
    subprocess.run([
        "yt-dlp",
        "--cookies", str(COOKIES_FILE),
        "--flat-playlist",
        "--print", "%(id)s",
        LIKED_PLAYLIST_URL
    ], stdout=id_file, stderr=subprocess.DEVNULL)

print("🔗 Generating video URLs...")
with open(IDS_FILE, "r") as f_in:
    ids = [line.strip() for line in f_in if line.strip()]

if not ids:
    print("⚠️ No video IDs were extracted. Check your cookies.txt or playlist access.")
    exit(1)

with open(URLS_FILE, "w") as f_out:
    for video_id in ids:
        f_out.write(f"https://www.youtube.com/watch?v={video_id}\n")

print(f"✅ {len(ids)} video URLs saved to {URLS_FILE}")
print(f"⬇️ Starting {MODE} download to: {TARGET_DIR}")

# Build yt-dlp command
command = [
    "yt-dlp",
    "--cookies", str(COOKIES_FILE),
    "--download-archive", str(ARCHIVE_FILE),
    "-o", str(TARGET_DIR / "%(title)s.%(ext)s"),
    "--batch-file", str(URLS_FILE)
]

if MODE == "audio":
    command += [
        "--extract-audio",
        "--audio-format", "mp3",
        "--audio-quality", "0"
    ]
else:
    command += [
        "--merge-output-format", "mp4"
    ]

result = subprocess.run(command)

if result.returncode != 0:
    print(f"⚠️ yt-dlp exited with warnings or errors during {MODE} download. Some files may be missing.")
else:
    print(f"✅ {MODE.capitalize()} download complete.")
