import re

class Convenciones:
    "Clase encargada de conocer las equivalencias de simbolos y hacer los reemplazos necesarios"

    operadores = {
        "SiSoloSi" : {
            "tipo" : "EOE",
            "asociativo" : False,
            "prioridad" : 1,
            "simbolos" : ["<=>","<->"]
        },
        "Implica" : {
            "tipo" : "EOE",
            "asociativo" : False,
            "prioridad" : 2,
            "simbolos" : ["=>","->"]
        },
        "Y" : {
            "tipo" : "EOE",
            "asociativo" : True,
            "prioridad" : 3,
            "simbolos" : ["Y","y","^","&","AND","and"]
        },
        "O" : {
            "tipo" : "EOE",
            "asociativo" : True,
            "prioridad" : 3,
            "simbolos" : ["O","o","V","v","+","or","OR"]
        },
        "O Excluyente" : {
            "tipo" : "EOE",
            "asociativo" : True,
            "prioridad" : 3,
            "simbolos" : ["Ó","ó","xor","XOR"]
        },
        "Negacion" : {
            "tipo" : "OE",
            "asociativo" : True,
            "prioridad" : 4,
            "simbolos" : ["!", "~", "¬", "not", "NOT"]
        }
    }

    parentesis = {
        "Parentesis de apertura" : {
            "simbolos" : ["(","[","{"]
        },
        "Parentesis de cierre" : {
            "simbolos" :  [")","]","}"]
        }
    }

    equivalencias = {}
    for key in parentesis:
        equivalencias[key] = parentesis[key]["simbolos"]
    for key in operadores:
        equivalencias[key] = operadores[key]["simbolos"]

    simbolos = {}
    for key in equivalencias:
        simbolos[key] = equivalencias[key][0]

    prioridades = {}
    for name in operadores:
        prioridad = operadores[name]["prioridad"]
        if prioridad in prioridades:
            prioridades[prioridad] = prioridades[prioridad] + [name]
        else:
            prioridades[prioridad] = [name]

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
    def operadoresEnOrden (cls):
        lista = []
        valorMaximo = max(cls.prioridades.keys())
        for prioridad in range(valorMaximo+1):
            if prioridad in cls.prioridades:
                for nombre in cls.prioridades[prioridad]:
                    lista += [nombre] 
        return lista

class Operador:
    def __init__(self,tipoOperador,padre):
        self.padre = padre
        for key in Convenciones.operadores[tipoOperador]:
            setattr(self,key,Convenciones.operadores[tipoOperador][key])
        setattr (self,"simbolo",Convenciones.simbolos[tipoOperador])
        self.name = tipoOperador

    def poblar(self,elementos):
        if self.tipo == "EOE":
            izq,der = self.segmentarEOE(elementos)
        if self.tipo == "OE":
            izq,der = self.segmentarOE(elementos)
        try {
            expresionIzq = ExpresionTextual.ProcesarExpresionTextual(izq,self)
        }
        try {
            expresionDer = ExpresionTextual.ProcesarExpresionTextual(der,self)
        }
        self.procesadoConExito = True

    def segmentarEOE(self,elementos):
        elementosIzq = []
        elementosDer = []
        encontrado = False
        for elemento in elementos:
            if not encontrado:
                if not type(elemento) == str:
                    elementosIzq += [elemento]
                else:
                    ocurrencias = findOccurrences(self.simbolo,elemento)
                    if not ocurrencias:
                        elementosIzq += [elemento]
                    else: 
                        Izq = elemento[:ocurrencias[0]]
                        Der = elemento[ocurrencias[0]+len(self.simbolo):]
                        elementosIzq += [Izq]
                        elementosDer += [Der]
                        encontrado = True
            else:
                elementosDer += [elemento]
        return elementosIzq,elementosDer

    def segmentarOE(self,elementos):
        elementosDer = []
        assert type(elementos[0]) == str, "No puede haber un parentesis u otro objeto en el primer lugar de la expresion si se encontro un operador OE, antes de llegar aca se deberia validar sintaxis"
        assert findOccurrences(self.simbolo,elemento)[0] == 0, "No puede haber un simbolo que no sea el del operador en el primer lugar de la expresion si se encontro un operador OE, antes de llegar aca se deberia validar sintaxis" 
        elementos[0] = elementos[0][1:]
        elementos = [elemento for elemento in elementos if elemento] # Eliminamos los casilleros vacios para el caso particular de que haya una negacion de un parentesis
        return None, elementos

    def sintaxisValida(self,elementos):
        "Valida que la expresion recibida (sacando el contenido de los eventuales parentesis pueda segmentarse con la logica que corresponde al operador. Es muy similar el codigo al EOE excepto que tiene que no haber nada delante del operador."
        # Unificamos todo lo que es texto en un solo string (sacamos lo que esta dentro de un parentesis) para estudiar si no hay error de sintaxis o de prioridades en la expresion
        textoCompleto = elementosToTexto(elementos)
        texto = elementosToTextoSinParentesis(elementos)
        #Verificamos que no haya ambiguedades por haber mas de un operador diferente con la misma prioridad en la expresion.
        if not self.validarSintaxisPrioridad(texto,textoCompleto):
            return False
        # Verificamos que no haya mas de un operador del mismo tipo salvo que sea asociativo.
        if not self.validarSintaxisAsociativo(texto,textoCompleto):
            return False
        # Verificamos que tengo elementos delante y detras segun corresponda.
        if self.tipo == "EOE":
            if not self.validarSintaxisEOE(elementos,texto,textoCompleto):
                return False
        if self.tipo == "OE":
            if not self.validarSintaxisOE(elementos,texto,textoCompleto):
                return False
        return True

    def validarSintaxisEOE(self,elementos,texto,textoCompleto):
        ocurrencias = findOccurrences(self.simbolo,texto)
        for ocurrencia in ocurrencias:
            if ocurrencia == 0:
                if type(elementos[0]) ==str:
                    Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + self.simbolo + "' al principio de la expresión y este operador necesita algo que lo preceda.",self.name)
                    return False
            if ocurrencia == len(texto) - len(self.simbolo):
                if type(elementos[-1]) == str:
                    Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + self.simbolo + "' al final de la expresión y este operador necesita algo que lo suceda.",self.name)
                    return False
        return True

    def validarSintaxisOE(self,elementos,texto,textoCompleto):
        ocurrencias = findOccurrences(self.simbolo,texto)
        if (ocurrencias[0] != 0) or (type(elementos[0])!=str):
            Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + self.simbolo + "' que no esta al principio de la expresión ni consecutivo a otro.",self.name)
            return False
        keep = -1
        for ocurrencia in ocurrencias:
            if ocurrencia - keep != 1:
                Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + self.simbolo + "' que no esta al principio de la expresión ni consecutivo a otro.",self.name)
            keep = ocurrencia
            return False
        return True

    def validarSintaxisPrioridad(self,texto,textoCompleto):
        "Verificamos que no haya ambiguedades por haber mas de un operador diferente con la misma prioridad en la expresion."
        nombreOperadoresIgualPrioridad = Convenciones.prioridades[self.prioridad]
        if len (nombreOperadoresIgualPrioridad) > 1:
            for nombreOperadorIgualPrioridad in nombreOperadoresIgualPrioridad:
                if not self.name == nombreOperadorIgualPrioridad:
                    if findOccurrences(Convenciones.simbolos[nombreOperadorIgualPrioridad],texto):
                        Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro una ambiguedad porque junto al simbolo " + self.simbolo + " se encontro el simbolo " + Convenciones.simbolos[nombreOperadorIgualPrioridad] + " y ambos operadores comparten prioridad de aplicación.", self.name)
                        return False
        return True

    def validarSintaxisAsociativo(self,texto,textoCompleto):      
        "Verificamos que no haya mas de un operador del mismo tipo salvo que sea asociativo."
        ocurrencias = findOccurrences(self.simbolo,texto)
        if len (ocurrencias) > 1:
            if not self.asociativo:
                Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro mas de una ocurrencia del simbolo que corresponde al operador '" + self.simbolo + "' al mismo nivel de prioridad y no es un operador que conmute, la expresión es ambigua.", self.name)
                return False
            else:
                if self.tipo == "EOE":
                    keep = -2
                    for ocurrencia in ocurrencias:
                        if ocurrencia - keep == 1:
                            Mensajes.MensajeErrorSintaxis(textoCompleto,"Se encontro mas de una ocurrencia del operador '" + self.simbolo + "' a continuación de otra lo cual no permite evaluar la expresión.", self.name)
                            return False
                        keep = ocurrencia + len(self.simbolo) - 1
        return True

class ExpresionTextual:
    "Esta clase involucra el proceso de transformar un texto en un operador o una proposicion"

    name = "ExpresionTextual"
    #operadores = [Parentesis, SiSoloSi, Implica, Y, O, OExcluyente, Negacion, Proposicion]

    def __init__ (self,contenido,padre):
        self.contenido = contenido # Si todavia nunca se busco un parentesis contenido deberia ser str sino una lista con algun elemento del tipo Parentesis y el resto texto
        self.padre = padre
        self.resultado = self.procesar()
        return 

    def procesar(self):
        # Primero se procesa los parentesis salvo que ya venga una lista lo que por construccion implica que ya se buscaron parentesis antes y este paso se puede saltear.
        if type(self.contenido) == str:
            if Parentesis.sintaxisValida(self.contenido):
                self.contenido = Parentesis.aplicarOperador(self.contenido)
            #TODO ver si no tiene sentio terminar aca en caso de que solo quede un parentesis.
            else:
                return #TODO Ver como manejar errores, la idea seria que el mensaje de error se genere abajo pero no se rompa el programa.
        listaDeOperadores = Convenciones.operadoresEnOrden()
        for nombreOperador in listaDeOperadores:
            # Vemos si hay una ocurrencia en el texto sin parentesis
            texto = elementosToTextoSinParentesis(self.contenido)
            ocurrencias = findOccurrences(Convenciones.simbolos[nombreOperador],texto)
            if ocurrencias:
                operador = Operador(nombreOperador,padre)
                if operador.sintaxisValida(elementos):
                    operador.poblar(elementos)
                else:
                    pass # TODO ver como reportar errores
                self.contenido = [operador]
                
        # TODO aplicar la logica de proposicion
        # Aca ya deberia haber solo un elemento en la lista que sea el operador que corresponda
        assert len(self.contenido) == 1, "Error de logica de programacion, una vez que una expresion textual ya paso todos las evaluacion de todos los operadores posibles solo deberia quedar un elemento que sea un operador"
        self.contenido = self.contenido[0]
        """    Creo que esto hace mas lio que otra cosa. Servia para eliminar posibles parentesis redundantes, pero obliga a reconstruir toda la estructura de operadores con parentesis explicitos o hacer muy complicado preservar los parentesis manuales.
        if self.contenido.name == "Parentesis":
            return self.contenido.contenido
        else:
            return self.contenido
        """
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




elementos = ["lOa","ChaOuee"]
tipoOperador = "O"
operador = Operador(tipoOperador)

operador.validarSintaxisEOE(elementos)
print (segmentarEOE(elementos,operador))

#texto = "([hd ))"

#exp = ExpresionTextual.ExpresionInicial(texto)
#print (exp)


