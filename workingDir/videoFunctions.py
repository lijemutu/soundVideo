from __future__ import unicode_literals
#import youtube_dl
import json, os, glob,random,shutil

# S
#def ytExtension(url):
    # DESCARGAR ALL EL CONTENIDO DEL ENLACE, ALMACENAR LA INFORMACION DE CADA CANCION
    # O VIDEO EN UN JSON CON EL MISMO NOMBBRE 

    #data = {}
    #data = json.dumps(data)
    #ydl_opts = {"writeinfojson": [data]}
    #with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    #    ydl.download([url])
# S    
def removeSpaceQuotes():
    # ITERAR PARA CADA CANCION DESCARGADA
    for filename in os.listdir():
        # REMOVER TODAS LAS COMILLAS SENCILLAS DE LOS NOMBRES, YA QUE SON NECESARIAS PARA OTRO 
        # PROCESO
        os.rename(filename, filename.replace('\'', '').replace(' ', '_'))
# S
def licenseCheck(license):
        for info in os.listdir():
            if info.endswith(".json"):
                # CARGAR
                with open(info, "r") as read_it:
                    data = json.load(read_it)
                # PEGAR LA EXTENSION MP3
                nameSong = info[:-10] + ".mp3"
                # ?????
                #nameSong = nameSong[len(folder_name) + 1 :]
                # print(nameSong)
                # IMPRIMIR LA LICENCIA QUE TIENEN CADA CANCION O ARCHIVO
                #print(data["license"])
                # SI NO SON DE LICENCIA LIBRE SE ELIMINAN JUNTO CON LOS JSON 
                if data["license"] != "cc-by" and license==1:
                    
                    if os.path.isfile(nameSong) ==1: 
                        os.remove(nameSong)
                    if os.path.isfile(info) ==1: 
                        os.remove(info)

                    print("Removed:", nameSong)
                # print(data["license"],name)
# P    
def download_music(url,folder_name,license):
    
    #CREAR UN NUEVO FOLDER CON EL NOMBRE ALBUM
    if os.path.isdir(folder_name) == 0:
        os.mkdir(folder_name)
    # MOVERSE A DICHO FOLDER
    os.chdir(folder_name)
    # DESCARGAR CANCIONES/VIDEOS
    #ytExtension(url)
    # REMOVER CARACTERES PARA QUE NO INTERFIERAN EN NINGUN PUNTO 
    removeSpaceQuotes()
    # CHECAR LA LICENCIA DE LOS ARCHIVOS
    licenseCheck(license)

    os.chdir("..")
# S
def info_songs(song,counter):
    song = song[:-3]
    song = song + "info.json"
    #print(song)
    with open(song, "r") as read_it:
        data = json.load(read_it)
    with open(f'info{counter}', 'a') as outfile:
        print("Cancion: " +data["title"] + "\n" \
             "Artista: "+ data["uploader"] + "\n" ,file=outfile)

# S
def joinSongs(songSet,counter,songs_prefix,jsonInfo,crossFadeVar):
            # INFORMACION PARA EL FFMPEG      
            # -VN IGNORA VIDEO DEL STREAM
            # -FILTER_COMPLEX FILTRO USADO PARA EL FADE OUT ENTRE CANCIONES
            # [0][1] INGRESAN EL INPUT 1 Y EL INPUT 2 APLICA EL CROSSFADE Y LO MANDA A [A01]}
            # -MAP [A02] COMO SALIDA UTILIZA EL ULTIMO EN LOS FILTROS
            inputSongs = ""
            crossFade = ""
            for i in range(len(songSet)-1):
                if i == len(songSet)-2:
                    inputSongs += f"-i \"{songSet[i]}\" " + f"-i \"{songSet[i+1]}\" "
                    if jsonInfo == 1:
                        info_songs(songSet[i],counter)
                        info_songs(songSet[i+1],counter)
                else:
                    inputSongs += f"-i \"{songSet[i]}\" "
                    if jsonInfo == 1:
                        info_songs(songSet[i],counter)
                
                
                if i == 0:
                    crossFade += f"[0][1]acrossfade=d=10:c1=tri:c2=tri[a1];" 
                if i == len(songSet)-2 and i!=0 :
                    crossFade += f"[a{i}][{i+1}]acrossfade=d=10:c1=tri:c2=tri[a{i+1}]"
                if i != len(songSet)-2 and i != 0:
                    crossFade += f"[a{i}][{i+1}]acrossfade=d=10:c1=tri:c2=tri[a{i+1}];"
            if crossFadeVar == 1:
                cmd = f"ffmpeg {inputSongs} -vn \
                -filter_complex \"{crossFade}\" \
                                -map \"[a{len(songSet)-1}]\"  {songs_prefix}{counter}.mp3"
            else:
                cmd = f"ffmpeg {inputSongs}  {songs_prefix}{counter}.mp3"

            os.system(cmd)

# P
def compact_songs(folder_name,setsNumber,songs_prefix,jsonInfo,crossFadeVar):
        
    #DIRIGIRNOS AL FOLDER CON LAS CANCIONES
    if os.path.isdir(folder_name) == 0:
        raise ValueError("No folder with songs on that folder name")
    # MOVERSE A DICHO FOLDER
    os.chdir(folder_name)
    # BUSCAR LOS NOMBRES DE LAS CANCIONES

    file = glob.glob("*.mp3")
    file = [os.path.relpath(fil) for fil in file]

    # HACER SUBCONJUNTOS DE 3 CANCIONES EN 3 O HASTA DONDE SE PUEDA
    subList = [file[n : n + setsNumber] for n in range(0, len(file), setsNumber)]

    # CONTADOR
    counter = 1
    # ITERAR SOBRES LOS CONJUNTOS DE 3 CANCIONES
    for sets in subList:   
        joinSongs(sets,counter,songs_prefix,jsonInfo,crossFadeVar)
        counter+=1
    os.chdir('..')
# S
def gif_video_info(gif_video_folder):
    
    os.chdir(gif_video_folder)

    archivo = {}
    archivo['archivo'] = []
    archivo['extension'] = []
    archivo['usuario'] = []

    for file in os.listdir():
        if file.endswith(('.mp4','.gif')):
            print("Archivo:",file,"rellena lo siguiente:")
            Usuario = input("Usuario: ")
            #temp = {'archivo':file , 'extension': file[-3:], 'usuario':Usuario}
            archivo['archivo'].append(file)
            archivo['extension'].append(file[-3:])
            archivo['usuario'].append(Usuario)
    with open('gif_info.json', 'w') as outfile:
        json.dump(archivo, outfile)
    os.chdir("..")
# S
def info_song_video(video,song,jsonInfo):
    os.chdir("..")
    if os.path.isdir("gifs") == 0:        
        raise ValueError("No folder with songs on that folder name")
   
    os.chdir("gifs")
    counter = song[-5]
    with open("gif_info.json") as gif_info:
        video_info = json.load(gif_info)
    #print(video_info['archivo'][0])
    if jsonInfo == 1:
        with open(f"info{counter}", "a") as read_it:
            i = 0
            for usuario in video_info['usuario']:
                if video == video_info['archivo'][i]:
                    print(f"Animacion creada por el usuario {usuario}",file=read_it)
                i+=1
    os.chdir("..")
    return usuario
# S
def author_box(video,usuario):


    cmd = f"ffmpeg  -i {video} -vf drawtext=\"fontfile=\'coolvetica compressed rg.ttf\': \
    text='{usuario}': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.65: \
    x=w-tw-10:y=h-th-10\" -c:v libx264 -preset veryfast -y v{video}"
    print(cmd)
    os.system(cmd)
# P
def video_song_making(folder_name,folder_gif,song_prefix,video_prefix,jsonInfo):

    if os.path.isdir(folder_name) == 0:
        raise ValueError("No folder with songs on that folder name")
    if os.path.isdir(folder_gif) == 0:
        raise ValueError("No folder with videos or gifs on that name")
    if os.path.isdir("dump_gifs") == 0:
        os.mkdir("dump_gifs")


    os.chdir(folder_gif)
    # Busca todos los mp4 o gif disponibles
    video = glob.glob("*.mp4")
    video = video + glob.glob("*.gif")
    video = [os.path.abspath(fil) for fil in video]
    os.chdir("..")


    os.chdir(folder_name)
    #CONTADOR PARA LA ESCRITURA DE LOS VIDEOS
    counter = 1
    for cancion in os.listdir():
        checking = f"{song_prefix}{counter}.mp3"
        if cancion ==checking:
            if len(video) == 0:
                raise ValueError ("Not enough gifs or videos")
            chosen_video = random.choice(video)
            #COMANDO PARA ESCRIBIR EN TERMINAL
            #-STREAM LOOP -1 REPITE INDEFINIDAMENTE EL VIDEO
            # -C:V COPY NO REALIZA ENCODE DE VIDEO SINO UTILIZA YA EL PREDEFINIFO
            # -C:A LIBMP3LAME  CODEC DE AUDIO -Q:A 4 CALIDAD 4 DEL CODEC DE AUDIO 160KB/S
            # -SHORTEST ACABAR EL VIDEO TAN PRONTO ACABE LA MUSICA
            usuario = info_song_video(chosen_video,cancion,jsonInfo)
            os.chdir(folder_name)
            video_file =  f"{video_prefix}{counter}.mp4"
            cmd = f"ffmpeg -stream_loop -1 -i \"{chosen_video}\" -i \"{cancion}\" \
                -c:v copy -c:a libmp3lame -q:a 4  \
                -shortest {video_file}"

            #ESCRIBIR A TERMINAL
            print(os.listdir())
            os.system(cmd)

            author_box(video_file,usuario)
            counter+=1
            if os.path.isfile(video_file) ==1:
                video.remove(chosen_video)
                shutil.move(chosen_video,"dump_gifs")
    os.chdir("..")

def clean_all(folder_name,video_prefix):
    os.chdir(folder_name)
    for file in os.listdir():
        if file.startswith(f"v{video_prefix}"):
            continue    
        if file.startswith("info"):
            continue
        os.remove(file)