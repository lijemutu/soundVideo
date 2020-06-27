from __future__ import unicode_literals
#import youtube_dl
import json, os, glob,random,shutil
from videoFunctions import download_music
from videoFunctions import compact_songs
from videoFunctions import video_song_making
#from videoFunctions import ytExtension
from videoFunctions import removeSpaceQuotes,licenseCheck,info_song_video
from videoFunctions import info_songs,joinSongs,gif_video_info,author_box,clean_all

os.chdir("workingDir")

#url = "https://soundcloud.com/yurilorenzoremixesbrazil"
folder_name = "MusicaFree"
songs_prefix = "musicFree"
folder_gif = "gifs"
video_prefix = "musicFreeVideo"
onlyFolder = 0
fade = 0
#download_music(url,folder_name,0)
compact_songs(folder_name,3,songs_prefix,onlyFolder,fade)
gif_video_info(folder_gif)

fontName = "coolvetica compressed rg.ttf"
shutil.move(fontName,folder_name)

video_song_making(folder_name,folder_gif,songs_prefix,video_prefix,onlyFolder)
clean_all(folder_name,video_prefix)



   
