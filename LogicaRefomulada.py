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

    simbolos = {}

    for key in equivalencias:
        simbolos[key] = equivalencias[key][0]

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
            Mensajes.MensajeLog("Se ha reemplazado el texto: '" + textoOriginal + "' por el texto '" + texto + "' para usar los caracteres estandarizados")
        

class ExpresionTextual:
    "Esta clase involucra el proceso de transformar un texto en un operador o una proposicion"

    name = "ExpresionTextual"
    #operadores = [Parentesis, SiSoloSi, Implica, Y, O, OExcluyente, Proposicion]

    def __init__ (self,contenido,padre):
        self.operadores = [Parentesis] # Esto estaria bueno ponerlo en la clase Convenciones pero tengo un problema porque al ser static no los reconoce si no los defino mas arriba
        self.contenido = contenido
        self.padre = padre
        self.validada = False
        self.procesar()

    def procesar(self):
        for operador in self.operadores:
            if operador.name == "Parentesis":
                if type(self.contenido) == str:
                    if operador.sintaxisValida(self.contenido):
                        self.contenido = operador.aplicarOperador(self.contenido)
                    else:
                        return
                else:
                    pass
        # Aca falta chequear que quede un solo elemento y si es texto reemplazarlo por una proposicion
        self.validada = True

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
            return [texto]
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
        aperturas = findOccurrences(texto,cls.simboloApertura)
        cierres = findOccurrences(texto,cls.simboloCierre)
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
        return pares


    @classmethod
    def tablaDeVerdad(cls,p):
        assert type(p) == bool, "La tabla de verdad solo se puede construir con valores booleanos"
        return p

    # Empezamos los metodos que corresponden a las instancias y no a la clase.
    def __init__ (self,texto,padre=None):
        "Se crea un elemento a partir de un texto que esta dentro de un parentesis"
        self.padre = padre
        self.child = ExpresionTextual(texto,self)

    def toText(self):
        return Parentesis.simboloApertura + self.child.toText() + Parentesis.simboloCierre

    def evaluar(self):
        return self.tablaDeVerdad(self.child.evaluar())
    

class Mensajes:
    "Clase encargada de manejar la interfaz de mensajes al usuario. Esta como clase separada para poder adaptar el modo en que se presentan los mensajes segun el GUI usado."

    @classmethod
    def MensajeLog(cls,txt,level="Info"):
        print (txt)

    @classmethod
    def MensajeErrorLogico (cls,txt):
        print(txt)

    @classmethod
    def MensajeErrorSintaxis (cls,texto,error,tipoDeOperador):
        msg = "En la expresión '"+ texto +"' se encontro un error al buscar elementos del tipo " + tipoDeOperador + " donde se reporto el siguiente mensaje: '" + error +"'"
        print (msg)
    

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]












texto = "(hd)as(aa)o"

exp = ExpresionTextual(texto,None)



