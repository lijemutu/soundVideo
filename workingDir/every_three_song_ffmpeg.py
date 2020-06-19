import os, glob,json
# UNIR TRES CANCIONES ~9 MINUTOS CADA CANCION FINAL

def info_songs(song,counter):
    song = song[:-3]
    song = song + "info.json"
    #print(song)
    with open(song, "r") as read_it:
        data = json.load(read_it)
    with open(f'info{counter}', 'a') as outfile:
        print("Cancion: " +data["title"] + "\n" \
             "Artista: "+ data["uploader"] + "\n" ,file=outfile)

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


compact_songs("rogerperis",3,"rogerperis")




