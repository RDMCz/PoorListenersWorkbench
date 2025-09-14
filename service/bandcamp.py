import json
import urllib.parse
import urllib.request
from typing import Tuple

from bs4 import BeautifulSoup

__HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def get_all_links_from_music_grid(url_music_grid: str) -> Tuple[list[str], list[str]]:
    """
    Returns collection of URLs for individual items in artist discography. Output is separated
    into two lists because Otiel's BandcampDownloader currently downloads only the first 16 albums
    if you check "Download artist discography". That's why you may need all the other links to
    download the rest of the albums separately.

    :param url_music_grid: URL to Bandcamp artist's music grid

    :return: Two lists that contain URL strings for each release (album/single/...) in the grid.
             First list contains latest 16 releases, second list contains everything else.
    """
    urllib_request = urllib.request.Request(url_music_grid)

    # Bandcamp returns 403 Forbidden if we don't have proper headers
    for header_key, header_value in __HEADERS.items():
        urllib_request.add_header(header_key, header_value)

    urllib_response = urllib.request.urlopen(urllib_request).read().decode("utf-8")
    soup = BeautifulSoup(urllib_response, "html.parser")

    # Relative paths are used on Bandcamp's site so we concat them to the base link
    url_splitted = urllib.parse.urlsplit(url_music_grid)
    url_base_str = str(urllib.parse.urlunsplit(url_splitted._replace(path="", query="", fragment="")))

    # == First 16 albums in the music grid can be found easily ==
    result1 = []
    divs = soup.find_all("div", {"class": "art"})
    for div in divs:
        result1.append(url_base_str + div.parent["href"])

    # == Albums from no.17 and onward are part of a long string which is then supposed to be handled by clientside JS (?) ==
    result2 = []
    music_grid = (soup.find("ol", {"id": "music-grid"}))

    if music_grid and music_grid.has_attr("data-client-items"):
        # This should be True if we have more than 16 albums
        data_client_items = music_grid["data-client-items"]
        json_data = json.loads(data_client_items)
        for item in json_data:
            result2.append(url_base_str + item["page_url"])

    return result1, result2


# For testing/debug:
if __name__ == "__main__":
    results = get_all_links_from_music_grid("https://filthware.bandcamp.com/")
    text1 = "\n".join(results[0])
    text2 = "\n".join(results[1])
    print(text1)
    print(text2)
