import json
import urllib.request
from typing import Any, Dict, List, Optional

import jsonpath_ng
import yt_dlp
from bs4 import BeautifulSoup


def __get_nested_value_or_none(where: Any, what: List[str]) -> Optional[Any]:
    current_node = where
    for key in what:
        if isinstance(current_node, dict) and key in current_node:
            current_node = current_node[key]
        elif isinstance(current_node, list) and isinstance(key, int) and 0 <= key < len(current_node):
            current_node = current_node[key]
        else:
            return None
        if not current_node:
            return None
    return current_node


def __playlist_url_2_html(url: str) -> str:
    try:
        urllib_request = urllib.request.Request(url)
    except ValueError as err:
        return repr(err)

    urllib_response = urllib.request.urlopen(urllib_request).read().decode("utf-8")
    return urllib_response


def __html_2_yt_initial_data_str(html: str) -> Optional[str]:
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script")
    script_with_yt_initial_data = None

    for script in scripts:
        if "ytInitialData = {" in script.text:
            script_with_yt_initial_data = script.text

    if script_with_yt_initial_data:
        return script_with_yt_initial_data[script_with_yt_initial_data.find("{"):-1]

    return None


def __yt_initial_data_str_2_json_song_list(yt_initial_data_str: str) -> Optional[List[Any]]:
    try:
        json_object = json.loads(yt_initial_data_str)
    except json.decoder.JSONDecodeError:
        return None
    except TypeError:
        return None
    jsonpath_expr = jsonpath_ng.parse("$..playlistVideoListRenderer")
    matches = jsonpath_expr.find(json_object)
    if matches:
        return matches[0].value["contents"]
    return None


def __json_song_list_2_final_song_list(song_list: List[Any]) -> List[Dict]:
    result = []
    song_number = 0
    if song_list:
        for song in song_list:
            song_number += 1
            result_song = {"number": song_number}
            if "playlistVideoRenderer" in song:
                song_object = song["playlistVideoRenderer"]
                result_song["id"] = __get_nested_value_or_none(song_object, ["videoId"])
                result_song["title"] = __get_nested_value_or_none(song_object, ["title", "runs", 0, "text"])
                result_song["artist"] = __get_nested_value_or_none(song_object, ["shortBylineText", "runs", 0, "text"])
            result.append(result_song)
            break
    return result


def __download_final_song_list(songs: List[Dict]):
    base_link = "https://www.youtube.com/watch?v="
    for song in songs:
        if song["id"]:
            yt_opts = {
                "format": "bestaudio/best",
                "outtmpl": f"{song["number"]} - {song["artist"]} - {song["title"]}.%(ext)s",
                "postprocessors": [
                    {"key": "FFmpegExtractAudio", "preferredcodec": "mp3"},
                    {"key": "FFmpegMetadata", "add_metadata": True}
                ],
                "postprocessor_args": {
                    "ffmpeg": [
                        "-metadata", f"artist={song["artist"]}",
                        "-metadata", f"albumartist={song["artist"]}",
                        "-metadata", f"title={song["title"]}",
                        "-metadata", f"track={song["number"]}",
                        "-metadata", "album=album",
                        "-metadata", "year=0",
                        "-metadata", f"comment={song["id"]}",
                    ]
                }
            }
            ydl = yt_dlp.YoutubeDL(yt_opts)
            ydl.download(base_link + song["id"])


def test():
    with open("service/test2.html", "r", encoding="utf-8") as _f:
        _kok = _f.read()
    _json_object_str = __html_2_yt_initial_data_str(_kok)
    _json_song_list = __yt_initial_data_str_2_json_song_list(_json_object_str)
    _final_song_list = __json_song_list_2_final_song_list(_json_song_list)
    return _final_song_list


# For testing/debug:
if __name__ == "__main__":
    with open("test2.html", "r", encoding="utf-8") as f:
        kok = f.read()

    json_object_str = __html_2_yt_initial_data_str(kok)

    json_song_list = __yt_initial_data_str_2_json_song_list(json_object_str)

    final_song_list = __json_song_list_2_final_song_list(json_song_list)

    __download_final_song_list(final_song_list)
