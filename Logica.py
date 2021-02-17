
class EOE(Operador):
    
def totext(cls,expresion):
    return expresion.subexpresiones[0].totext() + cls.simbolo + expresion.subexpresiones[1].totext()

class SiSoloSi (EOE):

    name = "SiSoloSi"
    equivalencias = [["<=>","<->"]]
    asociativo = False
    simbolo = equivalencias[0][0]
    prioridad = 1

class Implica (EOE):

    name = "Implica"
    equivalencias = [["=>","->"]]
    asociativo = False
    simbolo = equivalencias[0][0]
    prioridad = 2

class Y (EOE):

    name = "Y"
    equivalencias = [["Y","y","^","&","AND","and"]]
    asociativo = True
    simbolo = equivalencias[0][0]
    prioridad = 3

class O (EOE):

    name = "O"
    equivalencias = [["O","o","V","v","+","or","OR"]]
    asociativo = True
    simbolo = equivalencias[0][0]
    prioridad = 3

class OExcluyente (EOE):

    name = "OExcluyente"
    equivalencias = [["Ó","ó","xor","XOR"]]
    asociativo = True
    simbolo = equivalencias[0][0]
    prioridad = 3

class Negacion(Operador):
    """
    Operador del tipo OE, como es el unico lo definimos aca

    """
    name="Negacion"
    equivalencias = [["!", "~", "¬", "not", "NOT"]]
    asociativo = False
    prioridad = 4  
    simbolo = equivalencias[0][0]

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
        if cls.contarOcurrencias(expresion.textoRemanente) > 1:
            MensajeError(expresion,cls,"En la expresion se encontro mas de un operador del tipo " + cls.simbolo + " y solo tiene sentido que haya uno al inicio de cada expresión o subexpresión logica.")
            return
        numeroDeElementoConSimbolo = -1
        for idx, elemento in enumerate(expresion.elementosTemporales):
            if type(elemento) == str:
                if elemento.count(cls.simbolo):
                    numeroDeElementoConSimbolo = idx
                    break
        if numeroDeElementoConSimbolo > 0:
            MensajeError(expresion,cls,"En la expresion se encontro un operador del tipo " + cls.simbolo + " a continuacion de una proposicion o subexpresión logica y lo cual es un error de sintaxis.")
            return
        indiceDeOcurrencia = expresion.elementosTemporales[numeroDeElementoConSimbolo].find(cls.simbolo)
        if indiceDeOcurrencia > 0:
            MensajeError(expresion,cls,"En la expresion se encontro un operador del tipo " + cls.simbolo + " a continuacion de una proposicion o subexpresión logica y lo cual es un error de sintaxis.")
            return
        post = expresion.elementosTemporales[numeroDeElementoConSimbolo][indiceDeOcurrencia+len(cls.simbolo):]
        if not post:
            MensajeError(expresion,cls,"En la expresion se encontro un operador del tipo " + cls.simbolo + " sin nada a continuación.")
            return
        expresion.elementosTemporales = []
        expresion.subexpresiones = [Expresion.crearsubexpresion([post],expresion)]
        expresion.operacion = cls
        expresion.continuarvalidacion = False



class Expresion:

    name = "Expresion"
    operadores = [Parentesis, SiSoloSi, Implica, Y, O, OExcluyente, Proposicion]

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

    def totext(self):
        texto = ""
        if self.operacion:
            if type(self.operacion) == Proposicion.name:
                pass
            else:
                return self.operacion.builtext(self.subexpresiones)
        else:
            texto += Parentesis.simboloApertura + self.texto + Parentesis.simboloCierre
            print ("warning: esto hay que modificarlo cuando este hecho todos los operadores incluyendo la proposicion porque ahi depende el numero y tipo de operadores se construye diferente. Por ej si es una proposicion no tiene sentido poner parentesis.")
        return texto
        
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
        

















def test(testeos,indice=0):
    if indice:
        if indice == -1:
            indice = len(testeos) - 1
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
    ["p<=>q",True],
    ["p<-><->q",False],
    ["p<=>(q)",True],
    ["p<=>(q)(p)",False],
    ["p<=>(((q)))",True],
    ["pop",True],
    ["p",True]
]

test(testeos)