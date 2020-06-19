import os, glob,json
album = "notoriustrp1"
os.chdir(album)
def author_box(folder_name,video,gif_folder):
    for video in os.listdir():
        if video.endswith(".mp4"):
    
            cmd = f"ffmpeg  -i {video} -vf drawtext=\"fontfile=\'coolvetica compressed rg.ttf\': \
            text='{gif_author}': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.65: \
            x=w-tw-10:y=h-th-10\" -c:a copy -y v{video}"
            #print(cmd)
            os.system(cmd)

