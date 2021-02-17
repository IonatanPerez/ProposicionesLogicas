import re
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        if not texto: raise ErrorLogico("En la función reemplazarcaracteres se espera que el texto de entrada no sea vacio",texto)
        textoOriginal = texto
        for key in cls.equivalencias:
            for char in cls.equivalencias[key][1:]:
                texto = texto.replace(char,cls.simbolos[key])
        texto = texto.replace(" ", "")
        if not textoOriginal == texto:
            Mensajes.MensajeAlUsuario("Se ha reemplazado la expresión: '" + textoOriginal + "' por la expresión '" + texto + "' para usar los caracteres estandarizados")
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
        self.tipo = Convenciones.operadores[tipoOperador]["tipo"]
        self.asociativo = Convenciones.operadores[tipoOperador]["asociativo"]
        self.prioridad = Convenciones.operadores[tipoOperador]["prioridad"]
        self.simbolos = Convenciones.operadores[tipoOperador]["simbolos"]
        self.simbolo = Convenciones.simbolos[tipoOperador]
        self.name = tipoOperador

    def aplicar(self,elementos):
        self.validarSintaxis(elementos)
        if self.tipo == "EOE":
            izq,der = self.segmentarEOE(elementos)
            self.expresionIzq = ExpresionTextual.ProcesarExpresionTextual(izq,self) # Solo en caso de que sea EOE hay expresion a la izquierda
        if self.tipo == "OE":
            izq,der = self.segmentarOE(elementos)
            self.expresionIzq = None
        self.expresionDer = ExpresionTextual.ProcesarExpresionTextual(der,self)

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
        if not type(elementos[0]) == str: raise ErrorLogico("No puede haber un parentesis u otro objeto en el primer lugar de la expresion si se encontro un operador OE, antes de llegar aca se deberia validar sintaxis",elementos)
        if not findOccurrences(self.simbolo,elementos[0])[0] == 0: raise ErrorLogico("No puede haber un simbolo que no sea el del operador en el primer lugar de la expresion si se encontro un operador OE, antes de llegar aca se deberia validar sintaxis",elementos)
        elementos[0] = elementos[0][1:]
        elementos = [elemento for elemento in elementos if elemento] # Eliminamos los casilleros vacios para el caso particular de que haya una negacion de un parentesis
        return None, elementos

    def validarSintaxis(self,elementos):
        "Valida que la expresion recibida (sacando el contenido de los eventuales parentesis pueda segmentarse con la logica que corresponde al operador. Es muy similar el codigo al EOE excepto que tiene que no haber nada delante del operador."
        # Unificamos todo lo que es texto en un solo string (sacamos lo que esta dentro de un parentesis) para estudiar si no hay error de sintaxis o de prioridades en la expresion
        textoCompleto = elementosToTexto(elementos)
        texto = elementosToTextoSinParentesis(elementos)
        # Nos fijamos que exista el simbolo del operador porque si no hay simbolo del operador despues no se puede aplicar (esto es un error de logica porque no se deberia llegar aca)
        ocurrencias = findOccurrences(self.simbolo,texto)
        if not ocurrencias: raise ErrorLogico("Se esta buscando validar un operador del tipo '" + self.name + "' y no existe el caracter '" + self.simbolo + "' en lo que se quiere validar. Revisar porque se hace esto.", elementos)
        self.validarSintaxisPrioridad(texto,textoCompleto)
        self.validarSintaxisAsociativo(texto,textoCompleto)
        if self.tipo == "EOE":
            self.validarSintaxisEOE(elementos,texto,textoCompleto)
        if self.tipo == "OE":
            self.validarSintaxisOE(elementos,texto,textoCompleto)
            
    def validarSintaxisEOE(self,elementos,texto,textoCompleto):
        ocurrencias = findOccurrences(self.simbolo,texto)
        for ocurrencia in ocurrencias:
            if ocurrencia == 0:
                if type(elementos[0]) == str:
                    raise ErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + self.simbolo + "' al principio de la expresión y este operador necesita algo que lo preceda.",self.name)
            if ocurrencia == len(texto) - len(self.simbolo):
                if type(elementos[-1]) == str:
                    raise ErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + self.simbolo + "' al final de la expresión y este operador necesita algo que lo suceda.",self.name)

    def validarSintaxisOE(self,elementos,texto,textoCompleto):
        ocurrencias = findOccurrences(self.simbolo,texto)
        if (ocurrencias[0] != 0) or (type(elementos[0])!=str):
            raise ErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + self.simbolo + "' que no esta al principio de la expresión ni consecutivo a otro.",self.name)
        keep = -1
        for ocurrencia in ocurrencias:
            if ocurrencia - keep != 1:
                raise ErrorSintaxis(textoCompleto,"Se encontro un operador del tipo '" + self.simbolo + "' que no esta al principio de la expresión ni consecutivo a otro.",self.name)
            keep = ocurrencia

    def validarSintaxisPrioridad(self,texto,textoCompleto):
        "Verificamos que no haya ambiguedades por haber mas de un operador diferente con la misma prioridad en la expresion."
        nombreOperadoresIgualPrioridad = Convenciones.prioridades[self.prioridad]
        if len (nombreOperadoresIgualPrioridad) > 1:
            for nombreOperadorIgualPrioridad in nombreOperadoresIgualPrioridad:
                if not self.name == nombreOperadorIgualPrioridad:
                    if findOccurrences(Convenciones.simbolos[nombreOperadorIgualPrioridad],texto):
                        raise ErrorSintaxis(textoCompleto,"Se encontro una ambiguedad porque junto al simbolo " + self.simbolo + " se encontro el simbolo " + Convenciones.simbolos[nombreOperadorIgualPrioridad] + " y ambos operadores comparten prioridad de aplicación.", self.name)

    def validarSintaxisAsociativo(self,texto,textoCompleto):      
        "Verificamos que no haya mas de un operador del mismo tipo salvo que sea asociativo y en ese caso que no haya dos operadores consecutivos (esto elevaria un error en la iteracion siguiente de la recurencia pero seria menos claro el mensaje de error de sintaxis)."
        ocurrencias = findOccurrences(self.simbolo,texto)
        if len (ocurrencias) > 1:
            if self.asociativo:
                if self.tipo == "EOE":
                    keep = -2 # Iniciamos en -2 para evitar que un operador en el borde eleve el error (deberia elevar el error sintaxis EOE, pero el mensaje de error es otro)
                    for ocurrencia in ocurrencias:
                        if ocurrencia - keep == 1:
                            raise ErrorSintaxis(textoCompleto,"Se encontro una ocurrencia del operador '" + self.simbolo + "' a continuación de otra lo cual no permite evaluar la expresión.", self.name)
                        keep = ocurrencia + len(self.simbolo) - 1
            else:
                raise ErrorSintaxis(textoCompleto,"Se encontro mas de una ocurrencia del simbolo que corresponde al operador '" + self.simbolo + "' al mismo nivel de prioridad y no es un operador que conmute, la expresión es ambigua.", self.name)

    def explicar(self):
        pass
    
class ExpresionTextual:
    "Esta clase involucra el proceso de transformar un texto en un operador o una proposicion"

    name = "ExpresionTextual"
    #operadores = [Parentesis, SiSoloSi, Implica, Y, O, OExcluyente, Negacion, Proposicion]

    def __init__ (self,elementos,padre):
        self.elementos = elementos # Si todavia nunca se busco un parentesis contenido deberia ser str sino una lista con algun elemento del tipo Parentesis y el resto texto
        self.padre = padre
        self.resultado = self.procesar()
        return 

    def procesar(self):
        # Primero se procesa los parentesis salvo que ya venga una lista lo que por construccion implica que ya se buscaron parentesis antes y este paso se puede saltear.
        if type(self.elementos) == str:
            self.elementos = Parentesis.buscarYreemplazar(self.elementos)
        if len (self.elementos) == 1: # O es un texto o es un parentesis, en caso de que haya un parentesis y texto alrededor habria mas de un elemento generados en el paso anterior o cuando sea que se haya buscado parentesis.
            if not type(self.elementos[0]) == str:
                operador = self.elementos[0]
                operador.padre = self.padre
                return operador
        listaDeOperadores = Convenciones.operadoresEnOrden()
        texto = elementosToTextoSinParentesis(self.elementos)
        for nombreOperador in listaDeOperadores:
            # Vemos si hay una ocurrencia en el texto sin parentesis
            ocurrencias = findOccurrences(Convenciones.simbolos[nombreOperador],texto)
            if ocurrencias:
                operador = Operador(nombreOperador,self.padre)
                operador.aplicar(self.elementos)
                return operador
        # Si no se encontro ningun operador por descarte lo que hay en la expresion deberia ser una proposicion.
        return Proposicion.aplicarOperador(self.elementos,self.padre)

    @classmethod
    def ProcesarExpresionTextual(cls,contenido,padre):
        expresion = ExpresionTextual(contenido,padre)
        return expresion.resultado

    @classmethod
    def ExpresionInicial(cls,texto):
        if "\\" in texto:
            raise ErrorSintaxis(texto,"El caracter '\\' es un caracter reservado y no puede ser parte de la expresión",cls.name)
        texto = Convenciones.reemplazarcaracteres(texto)
        texto = texto.replace(" ","")
        return ExpresionTextual.ProcesarExpresionTextual(texto,None)

    @classmethod
    def ExpresionInicialconDebug(cls,texto):
        try:
            if "\\" in texto:
                raise ErrorSintaxis(texto,"El caracter '\\' es un caracter reservado y no puede ser parte de la expresión",cls.name)
            texto = Convenciones.reemplazarcaracteres(texto)
            texto = texto.replace(" ","")
            print (ExpresionTextual.ProcesarExpresionTextual(texto,None))
        except ErrorLogico as error:
            print ("Se detecto un error en la logica de procesamiento de datos, contacte al desarrollador. Se detalla el error a continucación.")
            print (error.msg)
            print ("El contexto del error fue el siguiente:")
            print (error.contexto)
            logger.exception(error)
        except ErrorSintaxis as error:
            print ("Se interrumpio el proceso porque se detecto un error de sintaxis.")
            print (error.msg)
    
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
    def buscarYreemplazar(cls,texto):
        pares = cls.validarYbuscarPares(texto) # Esto es una validacion de sintaxis implicita
        out = []
        last = -1
        for par in pares:
            out = out + [texto[last+1:par[0]]]
            contenido = Parentesis(texto[par[0]+1:par[1]],None) # Por el momento el parentesis es huerfano pues no se sabe que operador lo incluye (depende de los textos que haya a los costados), en caso de que solo quede un parentesis la expresion textual deberia sobreescribir a su padre.
            out = out + [contenido]
            last = par[1]
        out = out + [texto[last+1:]]
        out = [item for item in out if item]
        return out

    @classmethod
    def validarYbuscarPares(cls,texto):
        "Busca pares de apertura/cierre y sus posiciones en el texto, y realiza todas las validaciones de sintaxis."
        # Primero buscamos los simbolos de apertura y cierre
        aperturas = findOccurrences(cls.simboloApertura,texto)
        cierres = findOccurrences(cls.simboloCierre,texto)
        # Chequeamos que coincidan en numero.
        if len(aperturas) != len(cierres):
            raise ErrorSintaxis(texto,"En la expresion se encontro una cantidad diferente de parentesis de apertura que de cierre.",cls.name)
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
                    raise ErrorSintaxis(texto,"En la expresion se encontro un parentesis de apertura antes que uno de cierre.",cls.name)
        for par in pares:
            if par[1] == par[0]+1:
                raise ErrorSintaxis(texto,"En la expresion se encontro un parentesis de apertura y cierre sin contenido.",cls.name)
        lastclose = -2
        for par in pares:
            if par[0] == lastclose + 1:
                raise ErrorSintaxis(texto,"En la expresion se encontro un parentesis de cierre y uno de apertura sin ninguna expresión entre medio.",cls.name)
            lastclose = par[1]
        return pares

    # Empezamos los metodos que corresponden a las instancias y no a la clase.
    def __init__ (self,texto,padre=None):
        "Se crea un Parentesis a partir de un texto que esta dentro de un parentesis."
        self.padre = padre
        self.contenido = ExpresionTextual.ProcesarExpresionTextual(texto,self)

    def toText(self):
        return Parentesis.simboloApertura + self.contenido.toText() + Parentesis.simboloCierre
    
class Proposicion:

    name = "Proposicion"
    listaDeProposiciones = []

    @classmethod
    def validarSintaxis(cls,elementos):
        if len(elementos) > 1:
            texto = elementosToTexto(elementos)
            for elemento in elementos:
                if elemento.name == Parentesis.name:
                    raise ErrorSintaxis(texto,"En la expresion se encontro un parentesis concatenado a una proposicion sin conector lógico de por medio.",Proposicion.name)
                else: 
                    raise ErrorLogico("Al tratar de validar una expresion como Proposicion hay dos elementos sin que uno sea un parentesis",elementos)
        else:
            if not type(elementos[0]) == str:
                raise ErrorLogico("Si hay un solo elemento en una proposicion debe ser texto",elementosToTexto)

    @classmethod
    def aplicarOperador(cls,elementos,padre):
        cls.validarSintaxis(elementos) # Solo pasa la validacion si hay un solo elemento que es texto
        texto = elementos[0]
        for propExistente in cls.listaDeProposiciones:
            if propExistente.texto == texto:
                propExistente.padres += [padre]
                return propExistente
        proposicion = Proposicion(texto,padre)
        cls.listaDeProposiciones += [proposicion]
        return proposicion

    def __init__(self,texto,padre):
        self.texto = texto
        self.valorVerdad = True
        self.padres = [padre]

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
    def MensajeAlUsuario (cls,msg):
        print(msg)

class ErrorSintaxis(Exception):
    "Clase que se encarga de manejar los errores de sintaxis"
    #TODO aca se podria vincular con la GUI.
    def __init__(self,expresion,error,nombreTipoDeOperador,*args,**kwargs):
        self.msg = "En la expresión '"+ expresion +"' se encontro un error al buscar elementos del tipo " + nombreTipoDeOperador + " donde se reporto el siguiente mensaje: '" + error +"'"
        super().__init__(self.msg,*args,**kwargs)
        #Mensajes.MensajeAlUsuario(self.msg)

class ErrorLogico(Exception):
    "Clase que se encarga de manejar los errores de programacion. Idealmente no deberia usarse, pero como la logica del algoritmo es compleja previene y explica donde hay situaciones que no deberia suceder. Es una especie de assert."
    #TODO aca se podria vincular con la GUI.
    def __init__(self,texto,contexto,*args,**kwargs):
        self.msg = texto
        self.contexto = contexto
        super().__init__(self.msg,*args,**kwargs)
        #Mensajes.MensajeAlUsuario(self.msg)

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
                raise ErrorLogico("Se esta queriendo sacar algo que no es un parentesis de una lista de elementos donde hay un objeto que no es un parentesis, esto no deberia pasar porque esta funcion solo sirve para estudiar o precesar una expersion ingnorando el contenido de los parentesis",elementos)
    return texto


def tests(caso):
    
    if caso == 1:
        # Probamos que este andando el raise
        elementos = ["hola","chau"] # No tiene que devolver error
        elementosToTextoSinParentesis (elementos)
        elementos = ["hola",Proposicion("hola",None),"chau"] # No tiene que devolver error
        elementosToTextoSinParentesis (elementos)
    if caso == 2: # Probamos la funcion elementosToTexto
        elementos = ["hola",Proposicion("cucu",None),"chau"]
        print (elementosToTexto(elementos))
        elementos = ["hola",Parentesis("cucu"),"chau"]
        print (elementosToTexto(elementos))
    if caso == 3: # Probamos que el assert con un Exception funciones como esperamos  (no funciona)
        Convenciones.reemplazarcaracteres("")
    if caso == 4: # Probamos que funciones bien la funcion reemplazarcaracteres
        Convenciones.reemplazarcaracteres("[Hay que calor")
    if caso == 5: # Probamos que valide bien los casos de error de sintaxis
        expresiones = ["p<=>p","<=>p","p<=>","p<=>q<=>p","p<=><=>p","p=>p","=>p","p=>","p=>q=>p","p=>=>p","p=>q<=>p"]
        for expresion in expresiones:
            ExpresionTextual.ExpresionInicialconDebug(expresion)

tests(5)

