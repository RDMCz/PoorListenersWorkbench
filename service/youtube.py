import json
import urllib.request
from typing import Any, List, Optional

import yt_dlp
from bs4 import BeautifulSoup
from jsonpath_ng import parse

__LINK = "https://www.youtube.com/playlist?list=OLAK5uy_ne3EKxf6uKkEC2AeV1iYV_ZCxOEN6Tg_Y"


def __nested_key_check(where: Any, what: List[str]) -> bool:
    return True


def __playlist_url_2_html(url: str) -> str:
    try:
        urllib_request = urllib.request.Request(__LINK)
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


def __yt_initial_data_str_2_song_list(json_object_str: str) -> Optional[List[Any]]:
    try:
        json_object = json.loads(json_object_str)
    except json.decoder.JSONDecodeError:
        return None
    except TypeError:
        return None
    jsonpath_expr = parse("$..playlistVideoListRenderer")
    matches = jsonpath_expr.find(json_object)
    if matches:
        return matches[0].value["contents"]
    return None


def __zpracuj_songy_z_listu(song_list: List[Any]) -> None:
    if song_list:
        for song in song_list:
            # print(json.dumps(song,indent=4))
            song_object = song["playlistVideoRenderer"]
            print(song_object["videoId"])
            print(song_object["title"]["runs"][0]["text"])
            print(song_object["shortBylineText"]["runs"][0]["text"])
            print("===")

            break

            base_link = "https://www.youtube.com/watch?v="
            ydl = yt_dlp.YoutubeDL()
            ydl.download(base_link + song_object["videoId"])


if __name__ == "__main__":
    with open("test2.html", 'r', encoding="utf-8") as f:
        kok = f.read()

    json_object_str = __html_2_yt_initial_data_str(kok)

    json_list = __yt_initial_data_str_2_song_list(json_object_str)

    __zpracuj_songy_z_listu(json_list)
