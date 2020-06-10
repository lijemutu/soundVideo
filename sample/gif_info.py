import os, glob,json
# ESTE CÓDIGO VA A CREAR UN ARCHIVO JSON CON LA INFORMACIÓN DE CADA ARCHIVO DE VIDEO
# COMO SE SELECCIONAN A MANO, LA ULTIMA PARTE DEL NOMBRE DEL ARCHIVO GUARDADO
# DEBE SER EL USUARIO AL CUAL ATRIBUIRLE EL CONTENIDO, POR LO QUE SE HARA EL 
# INPUT DE ESTA INFORMACIÓN MANUALMENTE
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






