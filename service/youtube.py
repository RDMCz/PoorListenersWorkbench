import json
import urllib.request
from typing import Any, Dict, List, Optional

import jsonpath_ng
import yt_dlp
from bs4 import BeautifulSoup

from constant.audiotag_strenum import AudioTag


def __get_nested_value_or_empty_string(where: Any, what: List[str]) -> Optional[Any]:
    """
    :param where: Structure of nested lists and dictionaries, likely from json.loads
    :param what: Path to nested value: list where int means list index and string means dict key
    :return: Requested value if path `what` is valid in structure `where`, else empty string ""
    """
    current_node = where
    for key in what:
        if isinstance(current_node, dict) and key in current_node:
            current_node = current_node[key]
        elif isinstance(current_node, list) and isinstance(key, int) and 0 <= key < len(current_node):
            current_node = current_node[key]
        else:
            return ""
        if not current_node:
            return ""
    return current_node


def __playlist_url_2_html(url: str) -> str:
    """Returns response HTML for given YouTube playlist URL."""
    try:
        urllib_request = urllib.request.Request(url)
    except ValueError as err:
        return repr(err)

    urllib_response = urllib.request.urlopen(urllib_request).read().decode("utf-8")
    return urllib_response


def __html_2_yt_initial_data_str(html: str) -> Optional[str]:
    """Returns string containing contents of 'ytInitialData' JSON object,
    that is found in given YouTube playlist HTML response."""

    # YouTube playlist HTML response contains bunch of scripts and not really anything else
    # One of the scripts has a big JSON with 'ytInitialData' object, which contains everything we need

    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")
    script_with_yt_initial_data = None

    for script in scripts:
        if "ytInitialData = {" in script.text:
            script_with_yt_initial_data = script.text

    if script_with_yt_initial_data:
        # Return the content of 'ytInitialData', we don't need anything else
        return script_with_yt_initial_data[script_with_yt_initial_data.find("{"):-1]

    return None


def __yt_initial_data_str_2_json_song_list(yt_initial_data_str: str) -> Optional[List[Any]]:
    """Returns song list (JSON str → list of dicts) for given 'ytInitialData' string."""
    try:
        json_object = json.loads(yt_initial_data_str)
    except json.decoder.JSONDecodeError:
        return None
    except TypeError:
        return None

    # Information about videos in playlist is located in nested object 'playlistVideoListRenderer.contents'
    jsonpath_expr = jsonpath_ng.parse("$..playlistVideoListRenderer")
    matches = jsonpath_expr.find(json_object)
    if matches:
        return matches[0].value["contents"]

    return None


def __json_song_list_2_final_song_list_before_user_edit(song_list: List[Any]) -> List[Dict[AudioTag, str]]:
    """Returns list of songs with only the information we need in the UI
    (YT video ID, track number, title, artist, album artist, year, album)
    for given 'playlistVideoListRenderer.contents'."""

    # 'playlistVideoListRenderer.contents' contains a list of 'playlistVideoRenderer' objects
    # which contain all the information we need in some of its many nested values

    result = []
    song_number = 0  # Position in playlist determines the track number ID3v2 tag
    if song_list:
        for song in song_list:
            song_number += 1
            result_song = {
                AudioTag.NUMBER: str(song_number),
                # Leave these blank for now and user can change it later in the UI
                AudioTag.ALBUMARTIST: "",
                AudioTag.YEAR: "",
                AudioTag.ALBUM: "",
                # We'll try to find id, title and artist in JSON:
            }
            if "playlistVideoRenderer" in song:
                song_object = song["playlistVideoRenderer"]

                result_song[AudioTag.ID] = (
                    __get_nested_value_or_empty_string(song_object, ["videoId"])
                )
                result_song[AudioTag.TITLE] = (
                    __get_nested_value_or_empty_string(song_object, ["title", "runs", 0, "text"])
                )
                result_song[AudioTag.ARTIST] = (
                    __get_nested_value_or_empty_string(song_object, ["shortBylineText", "runs", 0, "text"])
                )

            result.append(result_song)
    return result


def __download_final_song_list(songs: List[Dict[AudioTag, str]]):
    """Uses yt-dlp and FFmpeg to download and tag songs from given list."""
    base_link = "https://www.youtube.com/watch?v="
    for song in songs:
        if song[AudioTag.ID]:
            yt_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"_download/{song[AudioTag.NUMBER].zfill(2)} - {song[AudioTag.ARTIST]} - {song[AudioTag.TITLE]}.%(ext)s",
                "postprocessors": [
                    {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"},
                    {"key": "FFmpegMetadata", "add_metadata": True}
                ],
                "postprocessor_args": {
                    "ffmpeg": [
                        "-metadata", f"artist={song[AudioTag.ARTIST]}",
                        "-metadata", f"albumartist={song[AudioTag.ALBUMARTIST]}",
                        "-metadata", f"title={song[AudioTag.TITLE]}",
                        "-metadata", f"track={song[AudioTag.NUMBER]}",
                        "-metadata", f"album={song[AudioTag.ALBUM]}",
                        "-metadata", f"year={song[AudioTag.YEAR]}",
                        "-metadata", f"comment={song[AudioTag.ID]}",
                    ]
                }
            }
            ydl = yt_dlp.YoutubeDL(yt_opts)
            ydl.download(base_link + song[AudioTag.ID])


def get_song_list_from_youtube_playlist_url(url: str):
    """Returns list of songs presentable in the UI for given YouTube playlist URL."""
    html = __playlist_url_2_html(url)
    json_object_str = __html_2_yt_initial_data_str(html)
    json_song_list = __yt_initial_data_str_2_json_song_list(json_object_str)
    final_song_list_before_user_edit = __json_song_list_2_final_song_list_before_user_edit(json_song_list)
    return final_song_list_before_user_edit


def download_song_list(songs: List[Dict[AudioTag, str]], start_index: int):
    """Downloads and tags songs from given list. Starts at song with index `start_index`."""
    if start_index <= 0:
        __download_final_song_list(songs)
    else:
        if start_index < len(songs):
            __download_final_song_list(songs[start_index:])
        else:
            print("Index out of range")


# For testing/debug:
if __name__ == "__main__":
    pass
