# YouTube Likes Exporter

A script to download your liked YouTube videos or audio tracks using your own cookies and `yt-dlp`.

---

## 📁 Folder structure

```
.
├── export.py
├── cookies.txt
├── requirements.txt
├── README.md
└── output/
    ├── audio/                   # MP3 downloads
    ├── video/                   # MP4 downloads
    └── data/                    # Temporary and tracking files
        ├── liked_ids.txt
        ├── liked_urls.txt
        ├── downloaded_audio.txt
        └── downloaded_video.txt
```

---

## ⚙️ Setup

### 1. Install Python and ffmpeg

- Python 3.10+ required
- `ffmpeg` is needed to convert audio/video properly

#### 🪟 Windows — ffmpeg installation

1. Go to:  
   https://www.gyan.dev/ffmpeg/builds/

2. Download this:  
   `Release full → ffmpeg-release-full.zip`

3. Extract it to a permanent folder, e.g.:  
   `C:\ffmpeg`

4. Add `C:\ffmpeg\bin` to your system `PATH`:

   - Press `Win + S` and search “Edit system environment variables”
   - Click **Environment Variables**
   - Under **System variables**, select `Path` → Edit → New
   - Paste:
     ```
     C:\ffmpeg\bin
     ```

5. Click OK in all dialogs, restart any open terminals

6. Confirm with:

   ```powershell
   ffmpeg -version
   ```

   You should see version info if it worked.

#### 🐧 Linux

```bash
sudo apt install ffmpeg
```

#### 🍎 macOS

```bash
brew install ffmpeg
```

---

### 2. Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

`requirements.txt` content:

```
yt-dlp==2025.7.21
```

---

### 3. Export your YouTube cookies

1. Install [Get cookies.txt extension](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. Go to https://www.youtube.com
3. Open the extension → save cookies to `cookies.txt`
4. Place `cookies.txt` in the root of the project

---

## ▶️ Usage

Download **videos**:

```bash
python export.py
```

Download **MP3 audio** only:

```bash
python export.py --mp3
```

What it does:

- Loads your liked videos playlist (`LL`) using cookies
- Extracts all video IDs and URLs
- Automatically downloads only new items (based on tracking files)
- Saves to:
  - `output/video/` (MP4)
  - `output/audio/` (MP3)
  - `output/data/` (IDs, URLs, and archive files)

---

## 🔁 Re-downloading

The script uses separate archive files:

| Format | Archive file                  |
|--------|-------------------------------|
| Video  | `downloaded_video.txt`        |
| Audio  | `downloaded_audio.txt`        |

If these files don't exist, the script will **warn you** and download everything again.  
If they exist, only **new videos not listed** will be downloaded.

---

## 🔒 Cookies info

- Your liked videos (`LL`) playlist is private by default
- The script needs valid cookies to access it
- Cookies may expire after hours or days
- If the script extracts no videos or fails to download:
  - Re-export `cookies.txt` from your browser
  - Do **not log out** from YouTube or change sessions between runs

---

## 🧼 Resetting everything

To start from scratch:

- Delete `output/audio/` or `output/video/`
- Delete archive files in `output/data/`:
  - `downloaded_audio.txt`
  - `downloaded_video.txt`

On next run, the script will re-download all your liked videos or audios.

---

## 🧠 FAQ

### Will the script crash if some videos fail?

No. If a video is deleted, private, or there's a connection issue:

- `yt-dlp` will skip it and continue
- The script will warn you at the end if there were any issues

You can re-run the script later with updated cookies to try again.

---

## ✅ Requirements

- Python 3.10+
- ffmpeg in system PATH
- yt-dlp (`yt-dlp==2025.7.21`)

---

## 🔧 Tips

- Run the script regularly to stay up to date
- Use `--mp3` when you only want audio
- Keep your cookies fresh for best results

---

## ⚖️ Legal notice

This script uses your own exported browser cookies to access your private YouTube "Liked videos" playlist.  
It is intended **only for personal archival purposes**.

⚠️ You are solely responsible for complying with YouTube's [Terms of Service](https://www.youtube.com/t/terms) and any copyright laws in your country.  
Do **not** redistribute or share downloaded content unless you own the rights.

---

## 📝 License

This project is released under the [MIT License](LICENSE).