import subprocess
import sys
import os
import argparse
from pathlib import Path

LIKED_PLAYLIST_URL = "https://www.youtube.com/playlist?list=LL"
COOKIES_FILE = "cookies.txt"
OUTPUT_DIR = Path("output")
AUDIO_DIR = OUTPUT_DIR / "audio"
VIDEO_DIR = OUTPUT_DIR / "video"
URLS_FILE = Path("liked_urls.txt")
FAILED_FILE = Path("failed.txt")
DOWNLOADED_AUDIO_FILE = Path("downloaded_audio.txt")
DOWNLOADED_VIDEO_FILE = Path("downloaded_video.txt")


def extract_video_ids():
    print("📥 Extracting video IDs from your liked playlist...")

    command = [
        sys.executable, "-m", "yt_dlp",
        "--flat-playlist",
        "--cookies", COOKIES_FILE,
        "--print", "%(id)s",
        LIKED_PLAYLIST_URL
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        ids = result.stdout.strip().splitlines()
        return ids
    except subprocess.CalledProcessError as e:
        print("❌ Error extracting video IDs. Are your cookies expired?")
        print(e.stderr)
        return []


def download(urls, audio_only):
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

    downloaded_file = DOWNLOADED_AUDIO_FILE if audio_only else DOWNLOADED_VIDEO_FILE
    downloaded_set = set()
    if downloaded_file.exists():
        downloaded_set = set(downloaded_file.read_text().splitlines())

    urls_to_download = [url for url in urls if url not in downloaded_set]
    if not urls_to_download:
        print("✅ All videos already downloaded.")
        return

    print(f"⬇️ {len(urls_to_download)} videos to download...")

    output_template = str((AUDIO_DIR if audio_only else VIDEO_DIR) / "%(title).200s.%(ext)s")

    for url in urls_to_download:
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--no-playlist",
            "-o", output_template,
            url
        ]

        if audio_only:
            cmd += ["-x", "--audio-format", "mp3", "--audio-quality", "0"]

        try:
            subprocess.run(cmd, check=True)
            downloaded_set.add(url)
            downloaded_file.write_text('\n'.join(downloaded_set))
        except subprocess.CalledProcessError:
            with FAILED_FILE.open("a") as f:
                f.write(url + "\n")

    print("✅ Download complete.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mp3", action="store_true", help="Download audio only as MP3")
    parser.add_argument("--no-prompt", action="store_true", help="Download immediately without prompt")
    args = parser.parse_args()

    video_ids = extract_video_ids()
    if not video_ids:
        print("❌ No video IDs extracted.")
        return

    urls = [f"https://www.youtube.com/watch?v={vid}" for vid in video_ids]
    URLS_FILE.write_text('\n'.join(urls))
    print(f"🔗 {len(urls)} video URLs saved to {URLS_FILE}")

    if args.no_prompt:
        download(urls, args.mp3)
    else:
        choice = input("⬇️ Do you want to download the videos now? (y/n): ").strip().lower()
        if choice == "y":
            download(urls, args.mp3)
        else:
            print("👌 Download skipped. You can run the script later using the saved URLs.")


if __name__ == "__main__":
    main()
