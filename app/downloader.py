from yt_dlp import YoutubeDL
from app.format_manager import FormatManager
import os
import sys

# -----------------------------
# FFmpeg Path
# -----------------------------
if getattr(sys, "frozen", False):
    # Running from PyInstaller EXE
    BASE_DIR = sys._MEIPASS
else:
    # Running from source code
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FFMPEG_PATH = os.path.join(BASE_DIR, "ffmpeg")

class Downloader:

    @staticmethod
    def get_video_info(url):

        options = {
            "quiet": True,
            "skip_download": True,
            # "cookiesfrombrowser": ("chrome",)
        }

        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
            print(info.get("thumbnail"))

        # Get clean format list from FormatManager
        formats = FormatManager.get_formats(info)

        return {
            "title": info.get("title"),
            "channel": info.get("uploader"),
            "duration": info.get("duration"),
            "views": info.get("view_count"),
            "formats": formats,
            "thumbnail": info.get("thumbnail")
        }

    @staticmethod
    def download_video(url, format_id, download_folder="downloads", progress_callback=None):
        print("===== MY DOWNLOADER =====")

        os.makedirs(download_folder, exist_ok=True)

        def hook(data):
            print("HOOK:", data.get("status"))
            if progress_callback:
                progress_callback(data)

        # -----------------------------
        # MP3 Download
        # -----------------------------
        if format_id == "mp3":

            options = {
                "format": "bestaudio/best",
                "outtmpl": f"{download_folder}/%(title)s.%(ext)s",
                "progress_hooks": [hook],
                # "ffmpeg_location": FFMPEG_PATH,
                # "cookiesfrombrowser": ("chrome",),
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "320",
                    }
                ],
            }
            # Use bundled FFmpeg only on Windows EXE
        if getattr(sys, "frozen", False) and sys.platform.startswith("win"):
            options["ffmpeg_location"] = FFMPEG_PATH
            # print(options)
        # -----------------------------
        # Video Download
        # -----------------------------
        else:

            options = {
                "format": f"{format_id}+bestaudio/best",
                "outtmpl": f"{download_folder}/%(title)s.%(ext)s",
                "progress_hooks": [hook],
                "merge_output_format": "mp4",
                # "ffmpeg_location": FFMPEG_PATH,
                # "cookiesfrombrowser": ("chrome",),
                "quiet": True,
            }
        # Use bundled FFmpeg only on Windows EXE
        if getattr(sys, "frozen", False) and sys.platform.startswith("win"):
            options["ffmpeg_location"] = FFMPEG_PATH
            # print(options)
        with YoutubeDL(options) as ydl:
            ydl.download([url])