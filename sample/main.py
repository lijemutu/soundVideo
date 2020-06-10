from __future__ import unicode_literals
import youtube_dl, json, os, glob,random,shutil

def download_music(url,folder_name,license):
    
    # print(glob.glob("*"))
    #CREAR UN NUEVO FOLDER CON EL NOMBRE ALBUM
    if os.path.isdir(folder_name) == 0:
        os.mkdir(folder_name)
    # MOVERSE A DICHO FOLDER
    os.chdir(folder_name)

    # DESCARGAR ALL EL CONTENIDO DEL ENLACE, ALMACENAR LA INFORMACION DE CADA CANCION
    # O VIDEO EN UN JSON CON EL MISMO NOMBBRE 
    data = {}
    data = json.dumps(data)
    ydl_opts = {"writeinfojson": [data]}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # ITERAR PARA CADA CANCION DESCARGADA
    for filename in os.listdir():
        # REMOVER TODAS LAS COMILLAS SENCILLAS DE LOS NOMBRES, YA QUE SON NECESARIAS PARA OTRO 
        # PROCESO
        os.rename(filename, filename.replace('\'', '').replace(' ', '_'))
        

    # NECESITAMOS OBTENER LOS ARCHIVOS JSON
    print(os.listdir())
    # ITERAR PARA CADA JSON
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
    os.chdir("..")

def info_songs(song,counter):
    song = song[:-3]
    song = song + "info.json"
    #print(song)
    with open(song, "r") as read_it:
        data = json.load(read_it)
    with open(f'info{counter}', 'a') as outfile:
        print("Cancion: " +data["title"] + "\n" \
             "Artista: "+ data["uploader"] + "\n" ,file=outfile)

def info_song_video(video,song):
    os.chdir("..")
    os.chdir("gifs")
    counter = song[-1]
    i = 0
    with open("gif_info.json") as gif_info:
        video_info = json.load(gif_info)

    with open(f"info{counter}", "a") as read_it:
        for key, value in video_info:
            if value == video:

                author = video_info['material'][i]['usuario']
                i+=1
        print(f"Animación creada por el usuario {author}",file=read_it)
   

def compact_songs(folder_name,setsNumber,videos_name):
        
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
                
        if len(sets) == 4:
        # CREAR UN ARCHIVO TEMPORAL INGRESANDO LOS NOMBRES DE LOS CONJUNTOS DE TRES CANCIONES
            
            # INFORMACION PARA EL FFMPEG      
            # -VN IGNORA VIDEO DEL STREAM
            # -FILTER_COMPLEX FILTRO USADO PARA EL FADE OUT ENTRE CANCIONES
            # [0][1] INGRESAN EL INPUT 1 Y EL INPUT 2 APLICA EL CROSSFADE Y LO MANDA A [A01]}
            # -MAP [A02] COMO SALIDA UTILIZA EL ULTIMO EN LOS FILTROS
            info_songs(sets[0],counter)
            info_songs(sets[1],counter)
            info_songs(sets[2],counter)
            info_songs(sets[3],counter)

            cmd = f"ffmpeg -i \"{sets[0]}\" -i \"{sets[1]}\" -i \"{sets[2]}\" -i \"{sets[3]} -vn \
            -filter_complex \"[0][1]acrossfade=d=10:c1=tri:c2=tri[a01]; \
                            [a01][2]acrossfade=d=10:c1=tri:c2=tri[a02]; \
                            [a03][3]acrossfade=d=10:c1=tri:c2=tri[a03]\" \
                            -map [a03] {videos_name}{counter}.mp3"
            os.system(cmd)
            counter+=1



        if len(sets) == 3:
        # CREAR UN ARCHIVO TEMPORAL INGRESANDO LOS NOMBRES DE LOS CONJUNTOS DE TRES CANCIONES
            
            # INFORMACION PARA EL FFMPEG      
            # -VN IGNORA VIDEO DEL STREAM
            # -FILTER_COMPLEX FILTRO USADO PARA EL FADE OUT ENTRE CANCIONES
            # [0][1] INGRESAN EL INPUT 1 Y EL INPUT 2 APLICA EL CROSSFADE Y LO MANDA A [A01]}
            # -MAP [A02] COMO SALIDA UTILIZA EL ULTIMO EN LOS FILTROS
            info_songs(sets[0],counter)
            info_songs(sets[1],counter)
            info_songs(sets[2],counter)
            cmd = f"ffmpeg -i \"{sets[0]}\" -i \"{sets[1]}\" -i \"{sets[2]}\" -vn \
            -filter_complex \"[0][1]acrossfade=d=10:c1=tri:c2=tri[a01]; \
                            [a01][2]acrossfade=d=10:c1=tri:c2=tri[a02]\" \
                            -map [a02] {videos_name}{counter}.mp3"
            os.system(cmd)
            counter+=1

        elif len(sets)==2:
            
        # INFORMACION PARA EL FFMPEG        
        # -VN IGNORA VIDEO DEL STREAM
        # -FILTER_COMPLEX FILTRO USADO PARA EL FADE OUT ENTRE CANCIONES
        # [0][1] INGRESAN EL INPUT 1 Y EL INPUT 2 APLICA EL CROSSFADE Y LO MANDA A [A01]}
        # -MAP [A02] COMO SALIDA UTILIZA EL ULTIMO EN LOS FILTROS
            info_songs(sets[0],counter)
            info_songs(sets[1],counter)
            cmd = f"ffmpeg -i \"{sets[0]}\" -i \"{sets[1]}\" -vn \
                    -filter_complex \"[0][1]acrossfade=d=10:c1=tri:c2=tri[a01]\" \
                    -map [a01] {videos_name}{counter}.mp3"
            os.system(cmd)

            counter+=1

        else:
            pass
    os.chdir('..')

def video_song_making(folder_name,folder_gif,song_prefix,video_prefix):

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
            info_song_video(chosen_video,cancion)
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

def gif_video_info(gif_video_folder):
    
    os.chdir(gif_video_folder)

    archivo = {}
    archivo['material'] = []


    for file in os.listdir():
        if file.endswith(('.mp4','.gif')):
            print("Archivo:",file,"rellena lo siguiente:")
            Usuario = input("Usuario: ")
            archivo['material'].append({
                'archivo':file,
                'extension':'.mp4' ,
                'usuario': Usuario
        })

    with open('gif_info.json', 'w') as outfile:
        json.dump(archivo, outfile)

def author_box(video,gif_author):
    cmd = f"ffmpeg  -i {video} -vf drawtext=\"fontfile=\'coolvetica compressed rg.ttf\': \
    text='{gif_author}': fontcolor=white: fontsize=24: box=1: boxcolor=black@0.65: \
    x=w-tw-10:y=h-th-10\" -c:a copy -y v{video}"
    print(cmd)
    os.system(cmd)


#download_music("https://soundcloud.com/runtlalala","runt",0)
#compact_songs("runt",3,"runt") # ARREGLAR EL PARÁMETRO PARA SETSNUMBER = 4
#gif_video_info("gifs")
video_song_making("runt","gifs","runt","runt")
