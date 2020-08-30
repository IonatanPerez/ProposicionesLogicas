class Expresion:
            
    def __init__(self,input,reemplazar=False):
        self.operadores = [Parentesis()]
        if reemplazar:
            for operador in self.operadores:
                texto = operador.reemplazarCaracteres(texto)        
        if type(input) == str:
            self.texto = input
            self.elementos = [self.texto]
            self.proposiciones = {}
            self.mensajesError = []
        else:
            self.texto = self.expresiontotext(input)
            self.elementos = input
            self.recuperarProposiciones (input)
            self.recuperarErrores (input)
        self.validado = False
        self.validar()

    def validar(self):
        for operador in self.operadores:
            self.texto = operador.reemplazarCaracteres(self.texto)        
            operador.aplicarOperador(self)
        if len(self.mensajesError):
            for error in self.mensajesError:
                print (error.reportar())
        else:
            self.validado = True

    def totext(self):
        return self.texto

    def expresiontotext(self,input):
        texto = ""
        for elemento in input:
            texto = texto + elemento.totext()
        return texto

    def recuperarErrores (self,input):
        for elemento in input:
            if type(elemento) == Expresion:
                self.proposiciones.update(elemento.proposiciones)

    def recuperarProposiciones (self,input):
        for elemento in input:
            if type(elemento) == Expresion:
                self.mensajesError = self.mensajesError + elemento.mensajeError

class Proposicion:

    def __init__(self,texto):
        self.texto = texto

    
class MensajeError:

    def __init__(self,contexto,operacion,mensaje):
        self.contexto = contexto
        self.operacion = operacion
        self.mensaje = mensaje

    def reportar(self):
        return "En el la expresion " + self.contexto.texto + " se encontro un error al procesar un operador de tipo " + self.operacion.name + " que reporto el siguiente mensaje: " + self.mensaje

class Operador:

    name = "por definir"
    equivalencias = []

    def reemplazarCaracteres(self,texto):
        for subtipo in self.equivalencias:
            for char in subtipo[1:]:
                texto = texto.replace(char,subtipo[0])
        return texto


class Parentesis(Operador):

    equivalencias = [["(","[","{"],[")","]","}"]]
    prioridad = 0
    name = "Parentesis"

    def aplicarOperador (self,expresion):
        elementosNuevo = []
        for elemento in expresion.elementos:
            if type(elemento) == str:
                apertura = elemento.find(self.equivalencias[0][0])
                if apertura == -1:
                    if elemento.find(self.equivalencias[1][0]) == -1: 
                        elementosNuevo = elementosNuevo + [elemento]
                    else:
                        error = MensajeError(expresion,Parentesis,"Se encontro un parentesis de cierre sin su correspondiente parentesis de apertura.")
                        expresion.mensajesError.append(error)
                else:
                    cierre = elemento[::-1].find(self.equivalencias[1][0])
                    posicioncierre = len(elemento) - cierre
                    if cierre == -1:
                        error = MensajeError(expresion,Parentesis,"Se encontro un parentesis de apertura sin su correspondiente parentesis de cierre.")
                        expresion.mensajesError.append(error)
                    else:
                        elementosNuevo = elementosNuevo + [elemento[:apertura]] + [Expresion(elemento[apertura+1:posicioncierre-1])] + [elemento[posicioncierre:]]
            else:
                elementosNuevo = elementosNuevo + [elemento]
        expresion.elementos = elementosNuevo

class SiSoloSi(Operador):

    equivalencias = [["<=>","<->"]]
    prioridad = 1
    name = "SiSoloSi"

    def aplicarOperador(self,expresion):
        elementosNuevo = []



def tests():
    texto = "H(o[l))ay (chau)"
    expresion = Expresion(texto)

tests()