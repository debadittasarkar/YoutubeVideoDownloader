class FormatManager:

    @staticmethod
    def get_formats(info):

        formats = []
        seen = set()

        # ---------- Video ----------
        for f in info.get("formats", []):

            if f.get("vcodec") != "none":

                height = f.get("height")
                ext = f.get("ext")
                format_id = f.get("format_id")

                if height:

                    text = f"{height}p ({ext.upper()})"

                    if text not in seen:
                        seen.add(text)

                        formats.append({
                            "id": format_id,
                            "text": text
                        })

        # ---------- Audio ----------
        formats.append({
            "id": "mp3",
            "text": "🎵 MP3 (320 kbps)"
        })

        for f in info.get("formats", []):

            if f.get("vcodec") == "none":

                ext = f.get("ext")
                abr = f.get("abr")
                format_id = f.get("format_id")

                text = f"{ext.upper()} ({abr} kbps)"

                if text not in seen:
                    seen.add(text)

                    formats.append({
                        "id": format_id,
                        "text": text
                    })

        return formats