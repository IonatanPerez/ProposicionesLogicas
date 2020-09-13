def strcopy(text):
    textonuevo = (text+".")[:-1]
    return textonuevo

def prueba(texto):
    c = strcopy(texto)
    print (id(texto),id(c))

prueba("hola")