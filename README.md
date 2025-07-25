# youtube-likes-exporter

Export your liked YouTube videos and download them as audio (`.mp3`) or video files.

---

## 🚀 Features

- Extracts video links from your private "Liked videos" playlist
- Downloads audio only (`--mp3`) or full video (default)
- Avoids redownloading already processed videos
- Resumable: run it again anytime
- No YouTube API required

---

## ⚙️ Requirements

- [Python 3.8+](https://www.python.org/downloads/)
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp)
- [`ffmpeg`](https://ffmpeg.org/) (for audio extraction)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### ffmpeg on Windows

1. Download from https://www.gyan.dev/ffmpeg/builds/
2. Extract to e.g. `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH:
   - Open “Edit environment variables”
   - Add it to your user `Path` variable
4. Restart terminal and run:

```bash
ffmpeg -version
```

---

## 🔐 Exporting Cookies

Your Liked playlist is private. You need to export your cookies to access it.

1. Install the extension:  
   👉 [Get cookies.txt](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. Go to https://www.youtube.com while logged in
3. Click the extension → Download `cookies.txt`
4. Save it next to `export.py`

> ⚠️ Cookies expire quickly. You only need them for link extraction.

---

## 📁 Output structure

```
.
├── export.py
├── cookies.txt
├── liked_urls.txt
├── downloaded_audio.txt
├── downloaded_video.txt
├── failed.txt
└── output/
    ├── audio/   ← for .mp3
    └── video/   ← for .mp4/.webm
```

---

## 💻 Usage

```bash
python export.py
```

This will:

- Use `cookies.txt` to extract all liked video URLs
- Save them to `liked_urls.txt`
- Prompt to start downloading

---

### 🔧 Optional flags

| Flag          | Description                     |
|---------------|---------------------------------|
| `--mp3`       | Download audio only (MP3 format)|
| `--no-prompt` | Skip prompt, start download     |

Examples:

```bash
python export.py --mp3
python export.py --mp3 --no-prompt
python export.py --no-prompt
```

---

## ℹ️ Notes

- Already downloaded links are tracked in:
  - `downloaded_audio.txt` or `downloaded_video.txt`
- Failed downloads are logged in `failed.txt`
- Videos that are private, deleted, or restricted will be skipped silently
- You can safely rerun the script — it won’t redownload what's already saved

---

## 📄 License

MIT — see [LICENSE](LICENSE)
