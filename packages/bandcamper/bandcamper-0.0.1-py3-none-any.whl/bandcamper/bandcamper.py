import json
import re
from pathlib import Path
from time import sleep
from urllib.parse import urljoin
from urllib.parse import urlparse
from zipfile import ZipFile

import click
import requests
from bs4 import BeautifulSoup
from onesecmail import OneSecMail
from onesecmail.validators import FromAddressValidator

from bandcamper.metadata.utils import get_track_output_context
from bandcamper.metadata.utils import suffix_to_metadata
from bandcamper.screamo import Screamer
from bandcamper.utils import get_download_file_extension
from bandcamper.utils import get_random_filename_template
from bandcamper.utils import get_random_user_agent


class Bandcamper:
    """Represents .

    Bandcamper objects are responsible of downloading and organizing
    the music from Bandcamp, among with writing their metadata.
    """

    # Bandcamp subdomain and URL Regexes taken from the pick_subdomain step of creating an artist page.
    # Rules for subdomains are:
    #   - At least 4 characters long
    #   - Only lowercase letters, numbers and hyphens are allowed
    #   - Must not end with hyphen
    _BANDCAMP_SUBDOMAIN_PATTERN = r"[a-z0-9][a-z0-9-]{2,}[a-z0-9]"
    BANDCAMP_SUBDOMAIN_REGEX = re.compile(
        _BANDCAMP_SUBDOMAIN_PATTERN, flags=re.IGNORECASE
    )
    BANDCAMP_URL_REGEX = re.compile(
        r"(?:www\.)?" + _BANDCAMP_SUBDOMAIN_PATTERN + r"\.bandcamp\.com",
        flags=re.IGNORECASE,
    )

    # Bandcamp IP for custom domains taken from the article "How do I set up a custom domain on Bandcamp?".
    # Article available on:
    #   https://get.bandcamp.help/hc/en-us/articles/360007902973-How-do-I-set-up-a-custom-domain-on-Bandcamp-
    CUSTOM_DOMAIN_IP = "35.241.62.186"
    DOWNLOAD_FORMATS = [
        "aac-hi",
        "aiff-lossless",
        "alac",
        "flac",
        "mp3-128",
        "mp3-320",
        "mp3-v0",
        "vorbis",
        "wav",
    ]

    BANDCAMP_EMAIL_VALIDATOR = FromAddressValidator(r".+@email\.bandcamp\.com")

    def __init__(
        self,
        *urls,
        **kwargs,
    ):
        # TODO: properly set kwargs
        self.urls = set()
        self.fallback = kwargs.pop("fallback", True)
        self.force_https = kwargs.pop("force_https", True)
        self.proxies = {
            "http": kwargs.pop("http_proxy", None),
            "https": kwargs.pop("https_proxy", None),
        }
        self.headers = {"User-Agent": get_random_user_agent()}
        self.screamer = kwargs.pop("screamer", Screamer())
        for url in urls:
            self.add_url(url)

    def _request_or_error(self, method, url, **kwargs):
        proxies = {**self.proxies, **kwargs.pop("proxies", {})}
        headers = {**self.headers, **kwargs.pop("headers", {})}
        response = requests.request(
            method, url, proxies=proxies, headers=headers, **kwargs
        )
        response.raise_for_status()
        return response

    def _get_request_or_error(self, url, **kwargs):
        return self._request_or_error("GET", url, **kwargs)

    def _post_request_or_error(self, url, **kwargs):
        return self._request_or_error("POST", url, **kwargs)

    def _is_valid_custom_domain(self, url):
        response = self._get_request_or_error(url, stream=True)
        return response.raw._connection.sock.getpeername()[0] == self.CUSTOM_DOMAIN_IP

    def _add_urls_from_artist(self, source_url):
        response = self._get_request_or_error(source_url)
        base_url = "https://" + urlparse(source_url).netloc.strip("/ ")
        soup = BeautifulSoup(response.content, "lxml")
        for a in soup.find("ol", id="music-grid").find_all("a"):
            parsed_url = urlparse(a.get("href"))
            if parsed_url.scheme:
                url = urljoin(
                    f"{parsed_url.scheme}://" + parsed_url.netloc.strip("/ "),
                    parsed_url.path.strip("/ "),
                )
            else:
                url = urljoin(base_url, parsed_url.path.strip("/ "))
            self.urls.add(url)

    def add_url(self, name):
        if self.BANDCAMP_SUBDOMAIN_REGEX.fullmatch(name):
            url = f"https://{name.lower()}.bandcamp.com/music"
            self._add_urls_from_artist(url)
        else:
            parsed_url = urlparse(name)
            if not parsed_url.scheme:
                parsed_url = urlparse("https://" + name)
            elif self.force_https:
                parsed_url = parsed_url._replace(scheme="https")
            url = parsed_url.geturl()
            if self.BANDCAMP_URL_REGEX.fullmatch(
                parsed_url.netloc
            ) or self._is_valid_custom_domain(url):
                if parsed_url.path.strip("/ ") in ["music", ""]:
                    url = f"{parsed_url.scheme}://{parsed_url.netloc}/music"
                    self._add_urls_from_artist(url)
                else:
                    self.urls.add(url)
            else:
                raise ValueError(f"{name} is not a valid Bandcamp URL or subdomain")

    def _get_music_data(self, url):
        response = self._get_request_or_error(url)
        soup = BeautifulSoup(response.content, "lxml")
        data = json.loads(soup.find("script", {"data-tralbum": True})["data-tralbum"])
        data["art_url"] = soup.select_one("div#tralbumArt > a.popupImage")["href"]
        from_album_span = soup.select_one("span.fromAlbum")
        if from_album_span is not None:
            data["album_title"] = from_album_span.text
        return data

    def download_to_file(self, url, save_path, filename):
        with requests.get(
            url, stream=True, proxies=self.proxies, headers=self.headers
        ) as response:
            response.raise_for_status()
            file_ext = get_download_file_extension(response.headers.get("Content-Type"))
            file_path = Path(save_path)
            file_path.mkdir(parents=True, exist_ok=True)
            file_path /= filename.format(ext=file_ext)
            with file_path.open("wb") as file:
                with click.progressbar(
                    response.iter_content(chunk_size=1024),
                    length=int(response.headers.get("Content-Length")) // 1024,
                    label=file_path.name,
                ) as bar:
                    for chunk in bar:
                        file.write(chunk)
        return file_path

    def _free_download(self, url, destination, *download_formats):
        response = self._get_request_or_error(url)
        soup = BeautifulSoup(response.content, "lxml")
        download_data = json.loads(soup.find("div", id="pagedata")["data-blob"])
        downloadable = download_data["download_items"][0]["downloads"]
        downloaded_paths = []
        for fmt in download_formats:
            if fmt in downloadable:
                parsed_url = urlparse(downloadable[fmt]["url"])
                stat_path = parsed_url.path.replace("/download/", "/statdownload/")
                fwd_url = parsed_url._replace(path=stat_path).geturl()
                fwd_data = self._get_request_or_error(
                    fwd_url,
                    params={".vrs": 1},
                    headers={**self.headers, "Accept": "application/json"},
                ).json()
                if fwd_data["result"].lower() == "ok":
                    download_url = fwd_data["download_url"]
                elif fwd_data["result"].lower() == "err":
                    download_url = fwd_data["retry_url"]
                else:
                    self.screamer.error(f"Error downloading {fmt} from {fwd_url}")
                    continue
                file_path = self.download_to_file(
                    download_url, destination, get_random_filename_template()
                )
                if file_path.suffix == ".zip":
                    extract_to_path = file_path.parent / file_path.stem
                    with ZipFile(file_path) as zip_file:
                        zip_file.extractall(extract_to_path)
                    file_path.unlink()
                    downloaded_paths.append(extract_to_path)
                else:
                    downloaded_paths.append(file_path)
            else:
                self.screamer.error(f"{fmt} download not found", short_symbol=True)
        return downloaded_paths

    def _get_download_url_from_email(
        self,
        url,
        item_id,
        item_type,
        country="US",
        postcode="0",
        encoding_name="none",
        timeout=60,
    ):
        artist_subdomain = urlparse(url).netloc
        download_url = f"https://{artist_subdomain}/email_download"
        mailbox = OneSecMail.generate_random_mailbox(
            proxies=self.proxies, headers=self.headers
        )
        form_data = {
            "encoding_name": encoding_name,
            "item_id": item_id,
            "item_type": item_type,
            "address": mailbox.address,
            "country": country,
            "postcode": postcode,
        }
        response = self._post_request_or_error(download_url, data=form_data)
        if not response.json()["ok"]:
            raise ValueError(f"Email download request failed: {response.text}")
        msgs = []
        time_sleeping = 0
        while not msgs:
            if time_sleeping > timeout:
                raise ValueError(
                    "Bandcamp email not received. Try increasing the timeout."
                )
            sleep(1)
            time_sleeping += 1
            msgs = mailbox.get_messages(validators=[self.BANDCAMP_EMAIL_VALIDATOR])
        soup = BeautifulSoup(msgs[0].html_body, "lxml")
        return soup.find("a")["href"]

    def move_file(self, file_path, destination, output, output_extra, tracks, context):
        if file_path.suffix in suffix_to_metadata:
            context.update(get_track_output_context(file_path, tracks))
        else:
            output = output_extra
            context["filename"] = file_path.name
        move_to = destination / output.format(**context)
        move_to.parent.mkdir(parents=True, exist_ok=True)
        file_path.replace(move_to)
        return move_to

    def download_fallback_mp3(self, track_info, artist, album, destination):
        file_paths = []
        for track in track_info:
            if track.get("file"):
                file_paths.append(
                    self.download_to_file(
                        track["file"]["mp3-128"],
                        destination,
                        f"{artist} - {album} - {track['track_num']:02d} {track['title']}{{ext}}",
                    )
                )
        return file_paths

    def download_from_url(
        self, url, destination, output, output_extra, *download_formats
    ):
        self.screamer.info(f"Searching available downloads for URL {url}")
        destination = Path(destination)
        download_formats = set(download_formats)
        download_mp3 = False
        if "mp3-128" in download_formats:
            download_formats.remove("mp3-128")
            download_mp3 = True

        music_data = self._get_music_data(url)
        if music_data is None:
            self.screamer.error(f"Failed to get music data from {url}")
            return

        tracks = {
            track["track_num"]: track["title"] for track in music_data["trackinfo"]
        }
        artist = music_data["artist"]
        album = (
            music_data["current"]["title"]
            if music_data["item_type"] == "album"
            else music_data.get("album_title", "")
        )
        year = music_data["current"]["release_date"].split()[2]
        title = music_data["current"]["title"]
        downloading_str = f"Downloading {artist} - {title}"

        if music_data.get("freeDownloadPage"):
            self.screamer.success(f"Free download found! {downloading_str}")
            file_paths = self._free_download(
                music_data["freeDownloadPage"], destination, *download_formats
            )
        elif music_data["current"].get("require_email"):
            self.screamer.success(f"Email download found! {downloading_str}")
            download_url = self._get_download_url_from_email(
                url, music_data["id"], music_data["item_type"]
            )
            file_paths = self._free_download(
                download_url, destination, *download_formats
            )
        elif self.fallback or download_mp3:
            self.screamer.success(f"MP3-128 download found! {downloading_str}")
            file_paths = self.download_fallback_mp3(
                music_data["trackinfo"], artist, album, destination
            )
            download_mp3 = False
        else:
            raise ValueError(
                f"No free download found for {url}. Try setting fallback to True."
            )

        if download_mp3:
            file_paths.extend(
                self.download_fallback_mp3(
                    music_data["trackinfo"], artist, album, destination
                )
            )

        context = {
            "artist": artist,
            "album": album,
            "year": year,
        }
        for file_path in file_paths:
            if file_path.is_dir():
                for track_path in file_path.iterdir():
                    new_path = self.move_file(
                        track_path, destination, output, output_extra, tracks, context
                    )
                    self.screamer.success(
                        f"New file: {new_path}", verbose=True, short_symbol=True
                    )
                file_path.rmdir()
            else:
                new_path = self.move_file(
                    file_path, destination, output, output_extra, tracks, context
                )
                self.screamer.success(
                    f"New file: {new_path}", verbose=True, short_symbol=True
                )

    def download_all(self, destination, output, output_extra, *download_formats):
        for url in self.urls:
            self.download_from_url(
                url, destination, output, output_extra, *download_formats
            )
