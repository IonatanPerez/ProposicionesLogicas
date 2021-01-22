import re

class Convenciones:
    "Clase encargada de conocer las equivalencias de simbolos y hacer los reemplazos necesarios"

    equivalencias = {
        "Parentesis de apertura" : ["(","[","{"],
        "Parentesis de cierre" : [")","]","}"],
        "SiSoloSi": ["<=>","<->"],
        "Implica": ["=>","->"],
        "Y": ["Y","y","^","&","AND","and"],
        "O": ["O","o","V","v","+","or","OR"],
        "O excluyente": ["Ó","ó","xor","XOR"],
        "Negación": ["!", "~", "¬", "not", "NOT"]
    }

    prioridades = {
        0 : ["Parentesis de apertura","Parentesis de cierre"],
        1 : ["SiSoloSi"], 
        2 : ["Implica"],
        3 : ["Y", "O", "O excluyente"],
        4 : ["Negación"]
    }

    simbolos = {}

    for key in equivalencias:
        simbolos[key] = equivalencias[key][0]

    operadoresEOE {
        "SiSoloSi" : {
            "asociativo" : False
            "prioridad" : 1
        }
    }

    @classmethod
    def reemplazarcaracteres (cls,texto):
        "Este es el inicio del proceso porque los caracteres se reemplazan una sola vez. De este metodo sale una expresión o un None."
        
        # Mensaje de error y se devuelve None si no hay un texto a procesar.
        if not texto:
            Mensajes.MensajeLog("Se debe ingresar un texto para analizar.")
            return None

        textoOriginal = texto
        for key in cls.equivalencias:
            for char in cls.equivalencias[key][1:]:
                texto = texto.replace(char,cls.simbolos[key])
        if not textoOriginal == texto:
            Mensajes.MensajeLog("Se ha reemplazado la expresión: '" + textoOriginal + "' por la expresión '" + texto + "' para usar los caracteres estandarizados")
        return texto

    @classmethod
    def buscarPrioridad(cls,name):
        for key in cls.prioridades:
            if name in cls.prioridades[key]:
                return key
        Mensajes.MensajeErrorLogico("Se esta buscando la prioridad de un operador que no tiene definida la prioridad")
        return -1 #TODO hacer mejor manejo de errores.

class ExpresionTextual:
    "Esta clase involucra el proceso de transformar un texto en un operador o una proposicion"

    name = "ExpresionTextual"
    #operadores = [Parentesis, SiSoloSi, Implica, Y, O, OExcluyente, Negacion, Proposicion]

    def __init__ (self,contenido,padre):
        self.operadores = [Parentesis,Proposicion] # Esto estaria bueno ponerlo en la clase Convenciones pero tengo un problema porque al ser static no los reconoce si no los defino mas arriba
        self.contenido = contenido # Si tidavia nunca se busco un parentesis contenido deberia ser str sino una lista con algun elemento del tipo Parentesis y el resto texto
        self.padre = padre
        self.validada = False
        self.resultado = self.procesar()
        return 


    def procesar(self):
        for operador in self.operadores:
            if operador.name == "Parentesis": # Distingue porque el parentesis es el unico operador que se tiene que aplicar al principio y solo si hay texto. Podria pasar que la expresion herede una lista en ese caso significa que ya se evaluo el operador Parentesis en la estructrura padre donde se creo esa expresion textual.
                if type(self.contenido) == str:
                    if operador.sintaxisValida(self.contenido):
                        self.contenido = operador.aplicarOperador(self.contenido)
                    else:
                        return #TODO Ver como manejar errores, la idea seria que el mensaje de error se genere abajo pero no se rompa el programa.
            else:
                if operador.sintaxisValida(self.contenido):
                    self.contenido = operador.aplicarOperador(self.contenido)
                else:
                    return #TODO Ver como manejar errores, la idea seria que el mensaje de error se genere abajo pero no se rompa el programa.

        # Aca ya deberia haber solo un elemento en la lista que sea el operador que corresponda
        assert len(self.contenido) == 1, "Error de logica de programacion, una vez que una expresion textual ya paso todos las evaluacion de todos los operadores posibles solo deberia quedar un elemento que sea un operador"
        self.contenido = self.contenido[0]
        if self.contenido.name == "Parentesis":
            return self.contenido.contenido
        else:
            return self.contenido

    @classmethod
    def ProcesarExpresionTextual(cls,contenido,padre):
        expresion = ExpresionTextual(contenido,padre)
        return expresion.resultado

    @classmethod
    def ExpresionInicial(cls,texto):
        if "\\" in texto:
            Mensajes.MensajeErrorSintaxis(texto,"El caracter '\\' es un caracter reservado y no puede ser parte de la expresión",cls.name)
            return
        texto = Convenciones.reemplazarcaracteres(texto)
        texto = texto.replace(" ","")
        return ExpresionTextual.ProcesarExpresionTextual(texto,None)

class Parentesis:

    """
        Esta clase diferentes funciones

        - Verificar la sintaxis de un texto buscando y verificando que los parentesis de apertura y cierre sean coherentes,
        de eso se encargan las funciones sintaxisValida y buscarPares
        - Segmentar un texto en una lista de bloques donde el contenido de los parentesis dentro del texto original
        sea reemplazado por un bloque del tipo parentesis para que los demas operadores no busquen en los textos
        correspondientes al contenido de los parentesis.
        - Crear un objeto de tipo parentesis que tenga un metodo para reconstruir su contenido y que se pueda anidar
        dentro del resto de la estrucutra de la expresion.
    """
    name = "Parentesis"
    simboloApertura = Convenciones.simbolos["Parentesis de apertura"]
    simboloCierre = Convenciones.simbolos["Parentesis de cierre"]

    @classmethod
    def sintaxisValida(cls,texto):
        pares = cls.buscarPares(texto)
        if pares == -1:
            return False
        else:
            return True
    
    @classmethod
    def aplicarOperador(cls,texto):
        pares = cls.buscarPares(texto)
        if pares == -1:
            return [texto] # TODO esto deberia dar error, no un texto op creo que podria sacar todoi este bloque
        out = []
        last = -1
        for par in pares:
            out = out + [texto[last+1:par[0]]]
            contenido = Parentesis(texto[par[0]+1:par[1]],None)
            out = out + [contenido]
            last = par[1]
        out = out + [texto[last+1:]]
        out = [item for item in out if item]
        return out


    @classmethod
    def buscarPares(cls,texto):
        "Busca pares de apertura/cierre y sus posiciones en el texto, en caso de encontrar un error devuelve un -1."

        # Primero buscamos los simbolos de apertura y cierre
        aperturas = findOccurrences(cls.simboloApertura,texto)
        cierres = findOccurrences(cls.simboloCierre,texto)
        # Chequeamos que coincidan en numero.
        if len(aperturas) != len(cierres):
            Mensajes.MensajeErrorSintaxis(texto,"En la expresion se encontro una cantidad diferente de parentesis de apertura que de cierre.",cls.name)
            return -1
        # Buscamos los pares
        pares = []
        if aperturas:
            while len(aperturas) > 0:
                if aperturas[0] < cierres[0]:
                    if len(aperturas) == 1:
                        pares = pares + [[aperturas[0],cierres[0]]]
                        aperturas.pop(0)
                        cierres.pop(0)
                    else:
                        if aperturas[1] < cierres[0]:
                            aperturas.pop(1)
                            cierres.pop(0) 
                        else:
                            pares = pares + [[aperturas[0],cierres[0]]]
                            aperturas.pop(0)
                            cierres.pop(0)
                else:
                    Mensajes.MensajeErrorSintaxis(texto,"En la expresion se encontro un parentesis de apertura antes que uno de cierre.",cls.name)
                    return -1
        for par in pares:
            if par[1] == par[0]+1:
                Mensajes.MensajeErrorSintaxis(texto,"En la expresion se encontro un parentesis de apertura y cierre sin contenido.",cls.name)
                return -1
        lastclose = -2
        for par in pares:
            if par[0] == lastclose + 1:
                Mensajes.MensajeErrorSintaxis(texto,"En la expresion se encontro un parentesis de cierre y uno de apertura sin ninguna expresión entre medio.",cls.name)
                return -1
            lastclose = par[1]
        return pares #TODO manejar mensajes de error

    # Empezamos los metodos que corresponden a las instancias y no a la clase.
    def __init__ (self,texto,padre=None):
        """Se crea un elemento a partir de un texto que esta dentro de un parentesis. 
        Los objetos del tipo parentesis solo tienen una vida temporal corta durante la logica de analisis sintactico, no perduran en la estructura final."""
        self.padre = padre
        self.contenido = ExpresionTextual.ProcesarExpresionTextual(texto,self)

    def toText(self):
        return Parentesis.simboloApertura + self.contenido.toText() + Parentesis.simboloCierre
    
class Proposicion:

    name = "Proposicion"
    setDeProposiciones = set()

    @classmethod
    def sintaxisValida(cls,elementos):
        if len(elementos) > 1:
            texto = elementosToTexto(elementos)
            for elemento in elementos:
                if elemento.name == Parentesis.name:
                    Mensajes.MensajeErrorSintaxis(texto,"En la expresion se encontro un parentesis concatenado a una proposicion sin conector lógico de por medio.",Proposicion.name)
                    return False
                else: 
                    Mensajes.MensajeErrorLogico("Al tratar de validar una expresion como Proposicion hay dos elementos sin que uno sea un parentesis")
                    return False
        else:
            return True

    @classmethod
    def aplicarOperador(cls,elemento):
        elemento = elemento[0]
        if type(elemento) == str:
            for propExistente in cls.setDeProposiciones:
                if propExistente.texto == elemento:
                    return propExistente
            proposicion = Proposicion(elemento)
            cls.setDeProposiciones.add(proposicion)
            return [proposicion]
        else:
            return [elemento]
        
    def __init__(self,texto,valorVerdad=True,padre=None):
        self.texto = texto
        self.valorVerdad = True
        self.padre = padre

    def toText(self):
        return self.texto

    def evaluar(self):
        return self.valorVerdad

    def setValorVerdad(self,valorVerdad):
        assert type(valorVerdad) == bool, "La tabla de verdad solo se puede construir con valores booleanos"
        self.valorVerdad = valorVerdad

class Mensajes:
    "Clase encargada de manejar la interfaz de mensajes al usuario. Esta como clase separada para poder adaptar el modo en que se presentan los mensajes segun el GUI usado."

    @classmethod
    def MensajeLog(cls,txt,level="Info"):
        print (txt)

    @classmethod
    def MensajeErrorLogico (cls,txt):
        print(txt)

    @classmethod
    def MensajeErrorSintaxis (cls,expresion,error,nombreTipoDeOperador):
        msg = "En la expresión '"+ expresion +"' se encontro un error al buscar elementos del tipo " + nombreTipoDeOperador + " donde se reporto el siguiente mensaje: '" + error +"'"
        print (msg)

class SiSoloSi:
    "Clase que contiene la informacion especifica y el objeto SiSoloSi."
    asociativo = False
    tipo = "EOE"
    name ="SiSoloSi"
    simbolo = Convenciones.simbolos[name]
    prioridad = Convenciones.buscarPrioridad(name)

class Y:
    "Clase que contiene la informacion especifica y el objeto Y."
    asociativo = True
    tipo = "EOE"
    name ="Y"
    simbolo = Convenciones.simbolos[name]
    prioridad = Convenciones.buscarPrioridad(name)

def findOccurrences(substring, string):
    " Busca ocurrencias de un substring, el unico caracter no permitido es un '\\' por un problema con Regex y Python"
    if len(substring) == 1:
        return [i for i, letter in enumerate(string) if letter == substring]
    else:
        specials = [".","+","*","?","^","$","(",")","[","]","{","}","|"]
        for original in specials:
            reemplazo = "\\" + original
            substring = substring.replace(original, reemplazo)
        return [m.start() for m in re.finditer(substring, string)]
    
def elementosToTexto(elementos):
    texto = ""
    for elemento in elementos:
        if type(elemento) == str:
            texto = texto + elemento
        else:
            texto = texto + elemento.toText()
    return texto

def elementosToTextoSinParentesis(elementos):
    texto = ""
    for elemento in elementos:
        if type(elemento) == str:
            texto = texto + elemento
        else:
            if not elemento.name == Parentesis.name:
                Mensajes.MensajeErrorLogico("Se esta queriendo sacar parentesis de una lista de elementos donde hay un objeto que no es un parentesis, esto no deberia pasar porque esta funcion solo sirve para estudiar o precoesa una expersion ingnorando el contenido de los parentesis")
    return texto

def validarSintaxisEOE(elementos,Operador):
    "Valida que la expresion recibida (sacando el contenido de los eventuales parentesis pueda segmentarse con la logica que corresponde al operador."
    # Unificamos todo lo que es texto en un solo string (sacamos lo que esta dentro de un parentesis) para estudiar si no hay error de sintaxis o de prioridades en la expresion
    textoCompleto = elementosToTexto(elementos)
    texto = elementosToTextoSinParentesis(elementos)
    # Verificamos que no haya ambiguedades por haber mas de un operador diferente con la misma prioridad en la expresion.
    if len (Convenciones.prioridades[Operador.prioridad]) > 1:
        nombreOperadoresIgualPrioridad = Convenciones.prioridades[Operador.prioridad]
        for nombreOperador in nombreOperadoresIgualPrioridad:
            if not Operador.name == nombreOperador:
                if findOccurrences(Convenciones.simbolos[nombreOperador],texto):
                    Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro una ambiguedad porque junto al simbolo " + Operador.simbolo + " se encontro el simbolo " + Convenciones.simbolos[nombreOperador] + " y ambos operadores comparten prioridad de aplicación.", Operador.name)
                    return False
    # Verificamos que no haya mas de un operador del mismo tipo salvo que sea asociativo.
    ocurrencias = findOccurrences(Operador.simbolo,texto)
    if len (ocurrencias) > 1:
        if not Operador.asociativo:
            Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro mas de una ocurrencia del simbolo que corresponde al operador '" + Operador.simbolo + "' al mismo nivel de prioridad y no es un operador que conmute, la expresion es ambigua.", Operador.name)
            return False
        else:
            keep = -2
            for ocurrencia in ocurrencias:
                if ocurrencia - keep == 1:
                    Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro mas de una ocurrencia del operador '" + Operador.simbolo + "' a continuación de otra lo cual no permite evaluar la expresión.", Operador.name)
                    return False
                keep = ocurrencia + len(Operador.simbolo) - 1
    for ocurrencia in ocurrencias:
        if ocurrencia == 0:
            if type(elementos[0]) ==str:
                Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + Operador.simbolo + "' al principio de la expresión y este operador necesita algo que lo preceda.",Operador.name)
        if ocurrencia == len(texto) - len(Operador.simbolo):
            if type(elementos[-1]) == str:
                Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + Operador.simbolo + "' al final de la expresión y este operador necesita algo que lo suceda.",Operador.name)
    return True

def segmentarEOE(elementos,Operador):
    elementosIzq = []
    elementosDer = []
    encontrado = False
    for elemento in elementos:
        if not encontrado:
            if not type(elemento) == str:
                elementosIzq += [elemento]
            else:
                ocurrencias = findOccurrences(Operador.simbolo,elemento)
                if not ocurrencias:
                    elementosIzq += [elemento]
                else: 
                    Izq = elemento[:ocurrencias[0]]
                    Der = elemento[ocurrencias[0]+len(Operador.simbolo):]
                    elementosIzq += [Izq]
                    elementosDer += [Der]
                    encontrado = True
        else:
            elementosDer += [elemento]
    return elementosIzq,elementosDer

def poblarEOE 

elementos = ["laY<=>","CYhau"]
Operador = Y

validarSintaxisEOE(elementos,Operador)
aplicarEOE(elementos,Operador)

#texto = "([hd ))"

#exp = ExpresionTextual.ExpresionInicial(texto)
#print (exp)


