from __future__ import unicode_literals
import youtube_dl
import json
import os, glob

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

download_music("https://soundcloud.com/rogerperis","rogerperis",1)