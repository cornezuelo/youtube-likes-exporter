# 🎵 YouTube Likes Exporter

Export and download all your **liked videos** from YouTube as video or MP3 using your own cookies.

## ⚙️ Features

- ✅ Extracts video IDs and URLs from your "Liked videos" playlist  
- 🎧 Downloads audio as `.mp3` with `--mp3`  
- ♻️ Skips already downloaded content  
- 📁 Organizes output into `data/`, `output/audio/`, and `output/video/`

## 🚀 Requirements

- Python 3.10+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://ffmpeg.org/) (for MP3 conversion)
- YouTube `cookies.txt` file (see below)

Install dependencies:

```bash
pip install -r requirements.txt
```

## 📥 Export your YouTube cookies

1. Install the browser extension:  
   👉 [Get cookies.txt](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)

2. Go to `https://www.youtube.com`  
3. Export cookies as `cookies.txt` and place it in the project root

## 🧪 Usage

Run the script from the project folder:

```bash
python export.py
```

### Available parameters

- `--download` → download the videos/audio after extracting links  
- `--mp3` → download audio only in MP3 format  

Examples:

```bash
python export.py --download
python export.py --mp3 --download
```

## 📁 Project structure

```text
.
├── export.py                 # Main script
├── requirements.txt          # Python dependencies
├── cookies.txt               # YouTube auth cookies (ignored by Git)
├── data/                     # Internal tracking files
│   ├── liked_ids.txt         # Extracted YouTube video IDs
│   ├── liked_urls.txt        # Full video URLs from the liked playlist
│   ├── downloaded_audio.txt  # Audio downloads already completed
│   ├── downloaded_video.txt  # Video downloads already completed
│   └── failed.txt            # Log of failed downloads (manual review)
└── output/                   # Final downloaded media
    ├── audio/                # Extracted .mp3 files (if using --mp3)
    └── video/                # Downloaded video files (default mode)
```
> ℹ️ `data/failed.txt` is only a log for failed downloads. The script does **not** retry them automatically.

## 🧱 FFmpeg setup

You need `ffmpeg` available in your system PATH.

- Download from: https://ffmpeg.org/download.html  
- Extract and place the `bin/` folder somewhere like `C:\ffmpeg\bin`
- Add that folder to your **System PATH** environment variable
- Restart your terminal or VSCode

## ⚠️ Legal notice

This tool is provided for **personal use only**. Downloading content from YouTube may violate their [Terms of Service](https://www.youtube.com/t/terms).  
You are solely responsible for how you use this script.

## 📄 License

MIT — see `LICENSE`