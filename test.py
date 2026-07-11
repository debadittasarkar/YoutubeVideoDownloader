from app.downloader import Downloader

info = Downloader.get_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(info)