from __future__ import unicode_literals
import os
import youtube_dl
import time

def downloaddirect(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        name = info_dict.get('title', None)
        print(name)
        ydl_opts = {'outtmpl': name + '.mp4'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  