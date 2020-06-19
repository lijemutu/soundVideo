import os,glob,random ,shutil,json

def info_song_video(video,song):
    counter = song[-1]
    i = 0
    with open("gif_info.json") as gif_info:
        video_info = json.loads(gif_info)

    with open(f"info{counter}", "a") as read_it:
        for key, value in video_info:
            if value == video:

            author = video_info['material'][i]['usuario']
            i+=1
        print(f"Animación creada por el usuario {author}",file=read_it)
    
#CONVIERTE LAS CANCIONES YA JUNTADAS EN PARES O TERCIAS EN VIDEOS CON LA AYUDA DE UN GIF
def video_song_making(folder_name,folder_gif,song_prefix,video_prefix):
    pass
    if os.path.isdir(folder_name) == 0:
        raise ValueError("No folder with songs on that folder name")
    if os.path.isdir(folder_gif) == 0:
        raise ValueError("No folder with videos or gifs on that name")
    if os.path.isdir("dump_gifs") == 0:
        os.mkdir("dump_gifs")

    dump_gifs = os.path.abspath("dump_gifs")
    os.chdir(folder_gif)
    video = glob.glob("*.mp4")
    video = video + glob.glob("*.gif")
    video = [os.path.abspath(fil) for fil in video]
    os.chdir("..")
    os.chdir(folder_name)
    #ENLISTA TODOS LOS ARCHIVOS CON LA PARTÍCULA PRUEB

    #CONTADOR PARA LA ESCRITURA DE LOS VIDEOS
    counter = 1

    for cancion in os.listdir():
        if cancion.startswith(f"{video_prefix}"):
            chosen_video = random.choice(video)
            #COMANDO PARA ESCRIBIR EN TERMINAL
            #-STREAM LOOP -1 REPITE INDEFINIDAMENTE EL VIDEO
            # -C:V COPY NO REALIZA ENCODE DE VIDEO SINO UTILIZA YA EL PREDEFINIFO
            # -C:A LIBMP3LAME  CODEC DE AUDIO -Q:A 4 CALIDAD 4 DEL CODEC DE AUDIO 160KB/S
            # -SHORTEST ACABAR EL VIDEO TAN PRONTO ACABE LA MUSICA
            info_song_gif(chosen_video,cancion)
            video_file =  f"{video_prefix}{counter}.mp4"
            cmd = f"ffmpeg -stream_loop -1 -i {chosen_video} -i {cancion} \
                -c:v copy -c:a libmp3lame -q:a 4  \
                -shortest {video_file}"

            #ESCRIBIR A TERMINAL
            os.system(cmd)
            counter+=1
            if os.path.isfile(video_file) ==1:
                video.remove(chosen_video)
                shutil.move(chosen_video,dump_gifs)


video_song_making("rogerperis","gifs","rogerperis","rogerperis")