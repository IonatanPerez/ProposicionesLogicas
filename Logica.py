class Operador:
    "Clase correspondiente a un operador generico donde se definen las funciones comunes a todos."
    name = None
    equivalencias = []
    simbolo = None

    @classmethod
    def reemplazarCaracteres(cls,texto):
        "Busca los caracteres equivalentes y los reemplaza por el predeterminado."
        for subtipo in cls.equivalencias:
            for char in subtipo[1:]:
                texto = texto.replace(char,subtipo[0])
        return texto

class Parentesis(Operador):

    equivalencias = [["(","[","{"],[")","]","}"]]
    prioridad = 0
    name = "Parentesis"

    simboloApertura = equivalencias[0][0]
    simboloCierre = equivalencias[1][0]

    @classmethod
    def buscarPares(cls,expresion):
        "Busca las posiciones de los pares de parentesis o un -1 si hay error sintactico."
        assert len(expresion.elementosTemporales) == 1
        assert type(expresion.elementosTemporales[0]) == str
        texto = expresion.elementosTemporales[0]
        assert texto
        aperturas = []
        apertura = -1
        while texto[apertura+1:].find(cls.simboloApertura) != -1:
            if aperturas:
                offset = aperturas[-1]+1
            else:
                offset = 0
            apertura = texto[apertura+1:].find(cls.simboloApertura) + offset
            aperturas = aperturas + [apertura]
        cierres = []
        cierre = -1
        while texto[cierre+1:].find(cls.simboloCierre) != -1:
            if cierres:
                offset = cierres[-1]+1
            else:
                offset = 0
            cierre = texto[cierre+1:].find(cls.simboloCierre) + offset
            cierres = cierres + [cierre]
        if len(aperturas) != len(cierres):
            MensajeError(expresion,Parentesis,"En la expresion se encontro una cantidad diferente de parentesis de apertura que de cierre.")
            return -1
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
                    MensajeError(expresion,Parentesis,"En la expresion se encontro un parentesis de apertura antes que uno de cierre.")
                    return -1
        for par in pares:
            if par[1] == par[0]+1:
                MensajeError(expresion,Parentesis,"En la expresion se encontro un parentesis de apertura y cierre sin contenido.")
                return -1
        return pares

    @classmethod
    def aplicarOperador (cls,expresion):
        """
        Aplica el operador parentesis a una expresion, asume que es el primer operador aplicado.

        La funcion asumen que en elementosTemporales solo hay un texto y lo segmenta en funcion de los parentesis mas externos que encuentre colocando
        en la propiedad elementos de la expresion los segmentos de texto que queden fuera de los parentesis y expresiones nuevas para
        los parentesis que correspondan. 

        Parametros:
        expresion -- la expresion a analisar.

        Condiciones sintacticas que valida el operador:
        - Que los parentesis tengan consistencia en su apertura y cierre
        - Que los parentesis tengan contenido
        - Que no haya mas de un parentesis sin que quede texto fuera
        
        """        
        pares = cls.buscarPares(expresion)
        texto = expresion.elementosTemporales[0]
        expresion.elementosTemporales = []
        if pares == -1:
            return # Se vuelve sin aplicar nada porque hubo un error en la sintaxis de los parentesis.
        else:
            if len(pares) == 1:
                if ((pares[0][0] == 0) and (pares[0][1] == len(texto)-1)):
                    expresion.texto = expresion.texto[1:-1]
                    expresion.elementosTemporales = [texto]
                    return 
            remanente = texto
            for par in pares:
                pre = texto[len(texto)-len(remanente):par[0]]
                if pre:
                    expresion.elementos.append(texto[len(expresion.texto)-len(remanente):par[0]])
                contenido = texto[par[0]+1:par[1]]
                expresion.elementosTemporales.append(Expresion(contenido,expresion)) 
                remanente = texto[par[1]+1:]
            if remanente:
                expresion.elementosTemporales.append(remanente)
            expresion.updateTextoRemanente()
            if expresion.textoRemanente == "":
                MensajeError(expresion,Parentesis,"En la expresion se encontro mas de un parentesis sin ningun tipo de operador que los conecte.")

    @classmethod
    def saltear(cls,texto):
        if not texto.find(cls.simboloApertura) == -1:
            return False
        if not texto.find(cls.simboloCierre) == -1:
            return False
        return True

    @classmethod
    def contarOcurrencias(cls,texto):
        return True

class EOE(Operador):
    """
    Operador generico del tipo EOE que toma una expresion y la segmenta en algo del tipo Expresion Operador Expresion.

    Es una clase completamente estatica ya que no tiene sentido que haya instancias del operado que funciona siempre igual y es 
    independiente de los objetos (expresiones u proposiciones sobre los que actua)
    
    """
    name = "EOE"
    asociativo = None
    prioridad = None
    simbolo = None
    
    @classmethod
    def contarOcurrencias(cls,texto):
        "Cuenta cuantas ocurrencias del simbolo que corresponde al operador hay en un texto."
        numeroDeOcurrencias = 0
        while not texto.find(cls.simbolo) == -1:
            texto = texto.replace(cls.simbolo,"",1)
            numeroDeOcurrencias += 1
        return numeroDeOcurrencias

    @classmethod
    def aplicarOperador(cls,expresion):
        "Verifica que no haya errores de sintaxis en los elementos a procesar (que son una cadena de str y expresiones provenientes de parentesis) y luego segmenta segun corresponda genernado en la expresion que recibe las expresiones y el operador correspondiete."
        if cls.asociativo:
            for operador in expresion.operadores:
                if cls.prioridad == operador.prioridad and not cls.name == operador.name:
                    if operador.contarOcurrencias(expresion.textoRemanente):
                        MensajeError(expresion,cls,"En la expresion se encontro un operador del tipo " + cls.simbolo + " junto a otro de tipo " + operador.simbolo + " y es ambiguo cual se debe aplicar primero.")
                        return
        else:
            if cls.contarOcurrencias(expresion.textoRemanente) > 1:
                MensajeError(expresion,cls,"En la expresion se encontro mas de un operador del tipo " + cls.simbolo + " y es ambiguo cual se debe aplicar primero.")
                return

        numeroDeElementoConSimbolo = -1
        for idx, elemento in enumerate(expresion.elementosTemporales):
            if type(elemento) == str:
                if elemento.count(cls.simbolo):
                    numeroDeElementoConSimbolo = idx
                    break
        indiceDeOcurrencia = expresion.elementosTemporales[numeroDeElementoConSimbolo].find(cls.simbolo)
        pre = expresion.elementosTemporales[numeroDeElementoConSimbolo][:indiceDeOcurrencia]
        post = expresion.elementosTemporales[numeroDeElementoConSimbolo][indiceDeOcurrencia+len(cls.simbolo):]
        if pre:
            expresionIzquierda = expresion.elementosTemporales[:numeroDeElementoConSimbolo] + [pre]
        else:
            expresionIzquierda = expresion.elementosTemporales[:numeroDeElementoConSimbolo]
        if post:
            expresionDerecha = [post] + expresion.elementosTemporales[numeroDeElementoConSimbolo+1:]
        else:
            expresionDerecha = expresion.elementosTemporales[numeroDeElementoConSimbolo+1:]
        if not expresionIzquierda:
            MensajeError(expresion,cls,"No se encontró una expresion valida delante del operador " + cls.simbolo + ".")
            return
        if not expresionDerecha:
            MensajeError(expresion,cls,"No se encontró una expresion valida detras del operador " + cls.simbolo + ".")
            return
        expresion.elementosTemporales = []
        expresion.subexpresiones = [Expresion.crearsubexpresion(expresionIzquierda,expresion),Expresion.crearsubexpresion(expresionDerecha,expresion)]
        expresion.operacion = cls

    @classmethod
    def totext(cls,expresion):
        return expresion.subexpresiones[0].totext() + cls.simbolo + expresion.subexpresiones[1].totext()

class SiSoloSi (EOE):

    name = "SiSoloSi"
    equivalencias = [["<=>","<->"]]
    asociativo = False
    simbolo = equivalencias[0][0]
    prioridad = 1

class Expresion:

    name = "Expresion"
    operadores = [Parentesis]# , SiSoloSi]#, Implica, Proposicion]

    def __init__ (self,texto,padre):
        assert texto
        assert type(texto) == str
        self.texto = texto
        self.textoRemanente = texto
        self.padre = padre
        self.mensajesError = []
        self.operacion = None
        self.subexpresiones = None
        self.validado = False
        self.continuarvalidacion = True
        self.errorEnSubexpresion = False
        self.elementosTemporales = [self.texto]
        self.procesar()
        if self.errorEnSubexpresion:
            if padre:
                padre.errorEnSubexpresion = True
                padre.continuarvalidacion = False
        else:
            if self.mensajesError:
                for mensaje in self.mensajesError:
                    mensaje.reportar()
                if padre:
                    self.padre.errorEnSubexpresion = True
            else:    
                self.validado = True
        
    @classmethod
    def crearsubexpresion (cls,elementosTemporales,padre):
        "Transforma un subconjunto de elementos a medio procesar en el texto correspodiente para crear una subexpresion nueva."
        texto = cls.elementosAtexto(elementosTemporales)
        assert texto
        return Expresion(texto,padre)

    @classmethod
    def elementosAtexto(cls,elementosTemporales):
        texto = ""
        for item in elementosTemporales:
            if type(item) == str:
                texto += item
            else:
                texto += item.totext()
        return texto

    @classmethod
    def reemplazarCaracteres (cls,texto):
        "Reemplaza los caracteres de un texto asumiento que el texto fue ingresado por el usuario y hay diferentes equivalencias para los mismos simbolos"
        for operador in cls.operadores:
            texto = operador.reemplazarCaracteres(texto)
        return texto

    @classmethod
    def expresionInicial (cls,texto):
        "Es el punto de entreda al codigo, toma el texto del usuario e inicia el proceso."
        if not texto:
            print ("Se debe ingresar un texto para analizar")
            return
        textoOriginal = texto
        texto = cls.reemplazarCaracteres(texto)
        if not textoOriginal == texto:
            print ("Se ha reemplazado el texto: " + textoOriginal + " por el texto " + texto + " para usar los caracteres estandarizados")
        expresion = Expresion(texto,False)
        if expresion.validado:
            #print ("La expresion: " + textoOriginal + " ha pasado el proceso de procesamiento y validacion sintactica")
            pass
        else:
            pass
            #print ("La expresion: " + textoOriginal + " no ha pasado el proceso de procesamiento y validacion sintactica")
        return expresion

    def totext(self):
        raise NotImplementedError # No me queda claro para que la querria. 
        
    def procesar(self):
        for operador in self.operadores:
            if self.continuarvalidacion:
                if operador.contarOcurrencias(self.textoRemanente):
                    operador.aplicarOperador(self)
                    self.updateTextoRemanente()

    def updateTextoRemanente(self):
        self.textoRemanente = ""
        for item in self.elementosTemporales:
            if type(item) == str:
                self.textoRemanente += item
        
class MensajeError:
    "Clase que se crea cuando aparece un error en una expresión para explicarlo."
    def __init__(self,contexto,operador,mensaje):
        self.contexto = contexto
        self.contexto.continuarvalidacion = False
        self.operador = operador
        self.mensaje = mensaje
        self.contexto.mensajesError.append(self)

    def reportar(self):
        "Genera el texto que explica el error."
        print ("En la expresion " + self.contexto.texto + " se encontro un error al procesar un operador de tipo " + self.operador.name + " que reporto el siguiente mensaje: " + self.mensaje)


def test(testeos,indice=0):
    if indice:
        expresion = Expresion.expresionInicial(testeos[indice][0])
        deberiapasar (testeos[indice][1],expresion,testeos[indice][0])
        return
    for item in testeos:
        expresion = Expresion.expresionInicial(item[0])
        deberiapasar (item[1],expresion,item[0])

def deberiapasar(valorEsperado,expresion,texto):
    if valorEsperado == expresion.validado:
        pass
        #print ("El codigo funciono como se esperaba para el ejemplo: " + texto)
    else:
        print ("El codigo NO funciono como se esperaba para el ejemplo: " + texto)

testeos = [
    ["p",True],
    ["(p)",True],
    ["[p]",True],
    ["{p}",True],
    ["()",False],
    ["(Hola",False],
    ["Hola)",False],
    ["Hola)(Chau",False],
    ["(Hola)p",True], #Por ahora
    ["(Hola)(Chau)",False],
    ["((Hola)())g",False],
    ["p<=>q",True]
]

test(testeos)