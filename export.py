import os
import sys
import subprocess
import argparse
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).parent.resolve()
OUTPUT_DIR = BASE_DIR / "output"
AUDIO_DIR = OUTPUT_DIR / "audio"
VIDEO_DIR = OUTPUT_DIR / "video"
DATA_DIR = BASE_DIR / "data"

LIKED_IDS_FILE = DATA_DIR / "liked_ids.txt"
LIKED_URLS_FILE = DATA_DIR / "liked_urls.txt"
FAILED_FILE = DATA_DIR / "failed.txt"
DOWNLOADED_AUDIO_FILE = DATA_DIR / "downloaded_audio.txt"
DOWNLOADED_VIDEO_FILE = DATA_DIR / "downloaded_video.txt"

def ensure_directories():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def check_requirements(mp3: bool):
    if not Path("cookies.txt").exists():
        print("❌ Missing cookies.txt. Export your YouTube cookies and place them in the script folder.")
        sys.exit(1)

    if shutil.which("yt-dlp") is None:
        print("❌ yt-dlp not found. Install it with: pip install yt-dlp")
        sys.exit(1)

    if mp3 and shutil.which("ffmpeg") is None:
        print("⚠️  WARNING: ffmpeg not found. Audio extraction may not work properly.")

def extract_video_ids():
    print("📥 Extracting video IDs from your liked playlist...")
    command = [
        sys.executable, "-m", "yt_dlp",
        "--extractor-args", "youtube:player_client=web",
        "--flat-playlist",
        "--cookies", "cookies.txt",
        "--print", "%(id)s",
        "https://www.youtube.com/playlist?list=LL"
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("❌ Failed to extract video IDs.")
        print(e.stderr.strip())
        sys.exit(1)

    video_ids = result.stdout.strip().splitlines()
    if not video_ids:
        print("❌ No videos found. Check if your cookies are valid.")
        sys.exit(1)

    LIKED_IDS_FILE.write_text("\n".join(video_ids), encoding="utf-8")
    return video_ids

def generate_video_urls(video_ids):
    urls = [f"https://www.youtube.com/watch?v={vid}" for vid in video_ids]
    LIKED_URLS_FILE.write_text("\n".join(urls), encoding="utf-8")
    print("🔗 Generating video URLs...")
    print("✅ Video URLs saved to", LIKED_URLS_FILE)
    return urls

def load_downloaded(file):
    return set(file.read_text(encoding="utf-8").splitlines()) if file.exists() else set()

def save_downloaded(file, video_id):
    with file.open("a", encoding="utf-8") as f:
        f.write(f"{video_id}\n")

def save_failed(url):
    with FAILED_FILE.open("a", encoding="utf-8") as f:
        f.write(f"{url}\n")

def download(urls, mp3=False):
    downloaded_audio = load_downloaded(DOWNLOADED_AUDIO_FILE)
    downloaded_video = load_downloaded(DOWNLOADED_VIDEO_FILE)

    for url in urls:
        video_id = url.split("=")[-1]
        if mp3 and video_id in downloaded_audio:
            continue
        if not mp3 and video_id in downloaded_video:
            continue

        output_template = AUDIO_DIR / "%(title).200s.%(ext)s" if mp3 else VIDEO_DIR / "%(title).200s.%(ext)s"
        command = [
            sys.executable, "-m", "yt_dlp",
            "--extractor-args", "youtube:player_client=web",
            "--cookies", "cookies.txt",
            "-o", str(output_template),
            url
        ]
        if mp3:
            command += ["-x", "--audio-format", "mp3"]

        try:
            subprocess.run(command, check=True)
            if mp3:
                save_downloaded(DOWNLOADED_AUDIO_FILE, video_id)
            else:
                save_downloaded(DOWNLOADED_VIDEO_FILE, video_id)
        except subprocess.CalledProcessError:
            save_failed(url)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mp3", action="store_true", help="Download audio only as MP3")
    parser.add_argument("--download", action="store_true", help="Download now after extracting")
    args = parser.parse_args()

    ensure_directories()
    check_requirements(mp3=args.mp3)
    video_ids = extract_video_ids()
    urls = generate_video_urls(video_ids)

    if args.download:
        print("📦 Downloading...")
        download(urls, mp3=args.mp3)
        print("✅ Download complete.")
    else:
        print("⬇️  Do you want to download the videos now? (y/n):", end=" ")
        if input().strip().lower() == "y":
            print("📦 Downloading...")
            download(urls, mp3=args.mp3)
            print("✅ Download complete.")
        else:
            print("👌 Download skipped. You can run the script later using", LIKED_URLS_FILE)

if __name__ == "__main__":
    main()