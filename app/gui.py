from app.downloader import Downloader
from app.thumbnail import Thumbnail
from customtkinter import CTkImage
from tkinter import filedialog
import customtkinter as ctk
import threading
import app.downloader


print(app.downloader.__file__)

def format_duration(seconds):

    if seconds is None:
        return "Unknown"

    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes:02}:{seconds:02}"


class YouTubeDownloaderApp(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.available_formats = {}

        self.title("YouTube Downloader")
        self.geometry("1000x700")

        self.download_folder = "downloads"

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.create_widgets()



    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="🎬 YouTube Downloader",
            font=("Arial", 30, "bold")
        )
        title.pack(pady=20)
        self.url_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.url_frame.pack(pady=10)

        self.url_entry = ctk.CTkEntry(
            self.url_frame,
            width=700,
            placeholder_text="Paste YouTube URL..."
        )
        self.url_entry.pack(side="left", padx=(0, 10))


        self.fetch_btn = ctk.CTkButton(
            self.url_frame,
            text="Fetch Video",
            width=120,
            command=self.fetch_video
        )
        self.fetch_btn.pack(side="left")

        # ---------------- Bottom controls (packed FIRST so they reserve space) ----------------

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)

        self.download_btn = ctk.CTkButton(
            self.bottom_frame,
            text="⬇ Download",
            command=lambda: threading.Thread(
                target=self.download_video,
                daemon=True
            ).start()
        )
        self.download_btn.pack(pady=10)

        self.progress = ctk.CTkProgressBar(
            self.bottom_frame,
            width=500
        )
        self.progress.pack(pady=10)
        self.progress.set(0)

        self.status = ctk.CTkLabel(
            self.bottom_frame,
            text="✅ Ready"
        )
        self.status.pack()

        # ---------------- Info frame (packed AFTER, fills remaining space) ----------------

        self.info_frame = ctk.CTkFrame(self)
        self.info_frame.pack(fill="both", expand=True, padx=20, pady=(20, 5))

        self.left_frame = ctk.CTkFrame(
            self.info_frame,
            fg_color="transparent"
        )

        self.left_frame.pack(
            side="left",
            padx=20,
            pady=20
        )

        self.right_frame = ctk.CTkFrame(
            self.info_frame,
            fg_color="transparent"
        )

        self.right_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.thumbnail_label = ctk.CTkLabel(
            self.left_frame,
            text=""
        )

        self.thumbnail_label.pack()

        self.title_label = ctk.CTkLabel(self.right_frame, text="Title :")
        self.title_label.pack(anchor="w", padx=20, pady=10)

        self.channel_label = ctk.CTkLabel(self.right_frame, text="Channel :")
        self.channel_label.pack(anchor="w", padx=20, pady=10)

        self.duration_label = ctk.CTkLabel(self.right_frame, text="Duration :")
        self.duration_label.pack(anchor="w", padx=20, pady=10)

        self.views_label = ctk.CTkLabel(self.right_frame, text="Views :")
        self.views_label.pack(anchor="w", padx=20, pady=10)

        self.format_label = ctk.CTkLabel(
            self.right_frame,
            text="Format"
        )

        self.format_label.pack(anchor="w", padx=20)

        self.format_menu = ctk.CTkOptionMenu(
            self.right_frame,
            values=["Fetch video first"]
        )

        self.format_menu.pack(anchor="w", padx=20, pady=10)

        # ---------------- Download Folder ----------------

        self.folder_label = ctk.CTkLabel(
            self.right_frame,
            text=f"📁 Folder : {self.download_folder}"
        )

        self.folder_label.pack(anchor="w", padx=20, pady=(20, 5))

        self.browse_btn = ctk.CTkButton(
            self.right_frame,
            text="📂 Browse Folder",
            command=self.choose_folder
        )

        self.browse_btn.pack(anchor="w", padx=20)
            

    def fetch_video(self):

        self.status.configure(text="🔍 Fetching Video...")

        url = self.url_entry.get()

        print("URL:", url)

        self.title_label.configure(text="Loading...")
        self.channel_label.configure(text="")
        self.duration_label.configure(text="")
        self.views_label.configure(text="")

        self.update()

        try:

            print("Calling downloader...")

            info = Downloader.get_video_info(url)

            # ---------- Thumbnail ----------
            image = Thumbnail.get_image(info["thumbnail"])

            self.thumbnail = CTkImage(
                light_image=image,
                dark_image=image,
                size=(300, 170)
            )

            self.thumbnail_label.configure(
                image=self.thumbnail,
                text=""
            )

            print("Downloader returned!")

            # ---------- Format values ----------
            duration = format_duration(info["duration"])
            views = f"{info['views']:,}"

            # ---------- Update Labels ----------
            self.title_label.configure(
                text=f"🎬 Title : {info['title']}"
            )

            self.channel_label.configure(
                text=f"👤 Channel : {info['channel']}"
            )

            self.duration_label.configure(
                text=f"⏱ Duration : {duration}"
            )

            self.views_label.configure(
                text=f"👁 Views : {views}"
            )

            # ---------- Format Dropdown ----------
            format_names = []

            self.available_formats = {}

            for item in info["formats"]:

                format_names.append(item["text"])

                self.available_formats[item["text"]] = item["id"]

            self.format_menu.configure(values=format_names)

            if format_names:
                self.format_menu.set(format_names[0])

            self.status.configure(text="✅ Ready")

            print("GUI Updated!")

        except Exception:
            import traceback
            traceback.print_exc()

            self.status.configure(text="❌ Failed")



    def download_video(self):
        print("🔥 Download button clicked")

        url = self.url_entry.get()

        try:

            self.progress.set(0)

            self.status.configure(text="Starting Download...")

            selected = self.format_menu.get()

            format_id = self.available_formats[selected]

            self.status.configure(text="⬇ Downloading...")

            Downloader.download_video(
                url,
                format_id,
                self.download_folder,
                self.progress_hook,
            )

        except Exception as e:

            self.status.configure(text=str(e))
    
    # def progress_hook(self, data):

        # if data["status"] == "downloading":

        #     downloaded = data.get("downloaded_bytes", 0)

        #     total = data.get("total_bytes") or data.get("total_bytes_estimate")

        #     if total:

        #         percent = downloaded / total
        #         print("Progress:", percent)

        #         def update_gui():
        #             self.progress.set(percent)
        #             self.status.configure(
        #                 text=f"{percent*100:.1f}% Downloading..."
        #             )

        #         self.after(0, update_gui)

        # elif data["status"] == "finished":

        #     self.after(
        #         0,
        #         lambda: self.status.configure(
        #             text="✅ Download Complete"
        #         )
        #     )

        #     self.after(
        #         0,
        #         lambda: self.progress.set(1)
        #     )
    
    def progress_hook(self, data):

        if data["status"] == "downloading":

            downloaded = data.get("downloaded_bytes", 0)

            total = data.get("total_bytes") or data.get("total_bytes_estimate")

            if total:

                percent = downloaded / total

                self.after(
                    0,
                    lambda p=percent: self.progress.set(p)
                )

                self.after(
                    0,
                    lambda p=percent: self.status.configure(
                        text=f"{p*100:.1f}% Downloading..."
                    )
                )

        elif data["status"] == "finished":

            self.after(
                0,
                lambda: self.progress.set(1)
            )

            self.after(
                0,
                lambda: self.status.configure(
                    text="✅ Download Complete"
                )
            )   

        

    def choose_folder(self):

        folder = filedialog.askdirectory()

        if folder:

            self.download_folder = folder

            self.folder_label.configure(
                text=f"📁 Folder : {folder}"
            )