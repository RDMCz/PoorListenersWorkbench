# Poor Listeners' Workbench

## What is this?

Yeah...

## Features

### _Bandcamp >16_

Otiel's [_BandcampDownloader_](https://github.com/Otiel/BandcampDownloader/) currently contains a bug that causes only the 16 most recent albums to be downloaded when you try to download an artist's entire discography. Since no one (myself included) has yet found the time and courage to fix the bug, I have created a simple tool to work around it. To download the complete discography, the first 16 albums can be downloaded as described above, and the rest must be entered into _BandcampDownloader_ one URL for each album. Rewriting these URLs can be tedious, especially if there are a lot of them.

This tool, called _Bandcamp >16_, receives a URL to the artist's "music grid" as input and outputs a list of all URLs for the artist's individual albums. You then just need to copy these URLs into _BandcampDownloader_ (and untick the "Download artist discography" option).

## Dependencies

* Python 3
* PySide 6&ensp;(LGPL)
* Beautiful Soup 4&ensp;(MIT)
* [h2non/jsonpath-ng](https://github.com/h2non/jsonpath-ng)&ensp;([Apache 2.0](https://github.com/h2non/jsonpath-ng/blob/master/LICENSE))
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)&ensp;([Unlicense](https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE))

## Law, Order, and Call to Action

Downloading music for personal use may not be legal where you live. Find out what your options are and (don't) use tools like this accordingly. If you want to support your favorite artists, buy their stuff on Bandcamp. If you are an artist worried about their work being "stolen", Bandcamp has [an answer](https://get.bandcamp.help/hc/en-us/articles/23020694039575-I-heard-you-can-steal-music-on-Bandcamp-What-are-you-doing-about-this) for you.

<b>"Why don't you just use Spotify?"</b>

There is a certain charm in maintaining your own offline music library. It comes with its own set of quirks, but has pros as well:

* No monthly subscription or ads
* No dependence on a third-party corporation (which may change its terms or go bankrupt)
* You don't have to worry about music that is missing from streaming platforms
* You can listen to music in higher quality
* If you like stats, you can still use Last.fm or ListenBrainz
  * These can also be used for discovering new music
* You can choose your own music player
* The directory structure allows for more flexible sorting than a set of playlists
* You can edit your audio files: maybe you really like only part of a song and don't like the rest, so you can just cut it out
* There are definitely more devices and HW/SW configurations that can play MP3 files than there are devices that can run the Spotify app

You could certainly compile a similar list of advantages of music streaming platforms or disadvantages of offline audio libraries. Just keep in mind that this option exists. Then there is also this somewhat darker problem with streaming services and music distributors: how they treat genuine independent artists while letting all kinds of scams and a flood of AI music slip through their fingers. There are many discussions on this issue. If you are interested, I think this video sums it up nicely: [It's Not Just You: Music Streaming Is Broken Now](https://youtu.be/plleJ0Zv0Ww) by Venus Theory.

The time is now! Become your own master! (At least when it comes to listening to music.)
