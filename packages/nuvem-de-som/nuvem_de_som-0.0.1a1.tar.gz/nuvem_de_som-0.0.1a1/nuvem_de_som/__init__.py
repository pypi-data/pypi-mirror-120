from bs4 import BeautifulSoup
import requests
import youtube_dl


class SoundCloud:
    @staticmethod
    def search(query, parse=True):
        url = "https://soundcloud.com/search/sounds?q=" + query
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for link in soup.find_all('h2'):
            r = link.find('a')
            url = r.get('href')
            if url.startswith("/"):
                url = "https://soundcloud.com" + url
            info = {
                "title": link.text,
                "url": url
            }
            if parse:
                info = SoundCloud._parse(url)
            yield info

    @staticmethod
    def _parse(track_url, prefered_ext=None):
        ydl_opts = {"quiet": True, "verbose": False}
        kmaps = {"duration": "duration",
                 "thumbnail": "image",
                 "uploader": "artist",
                 "title": "title",
                 'webpage_url': "url"}
        info = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(track_url, download=False)
            for k, v in kmaps.items():
                info[v] = meta[k]
            info["uri"] = meta["formats"][-1]["url"]
            if prefered_ext:
                for f in meta["formats"]:
                    if f["ext"] == prefered_ext:
                        info["uri"] = f["url"]
                        break
        return info

