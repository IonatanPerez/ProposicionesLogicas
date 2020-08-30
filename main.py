class Expresion:
    
    def __init__(self,texto):
        self.texto = texto
        self.proposiciones = []
        self.elementos = [texto]
        self.mensajesError = []

    def validar(self):
        pass

    def Atexto(self):
        pass


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
                    print (elemento)
                    print (apertura)
                    cierre = elemento[::-1].find(self.equivalencias[1][0])
                    if cierre == -1:
                        error = MensajeError(expresion,Parentesis,"Se encontro un parentesis de apertura sin su correspondiente parentesis de cierre.")
                        expresion.mensajesError.append(error)
                    else:
                        print (cierre)
                        elementosNuevo = elementosNuevo + [elemento[:apertura]] + [Expresion(elemento[apertura:len(elemento) - cierre])] + [elemento[cierre:]]
            else:
                elementosNuevo = elementosNuevo + [elemento]
        expresion.elementos = elementosNuevo

def tests():
    texto = "Hol)a"
    expresion = Expresion(texto)
    print (expresion.texto)
    print (expresion.elementos)
    print (expresion.mensajesError)
    parentesis = Parentesis()
    parentesis.aplicarOperador(expresion)
    parentesis.aplicarOperador(expresion)
    print (expresion.texto)
    print (expresion.elementos)
    print (expresion.mensajesError)
    print (expresion.mensajesError[0].reportar())


    #print (expresion.elementos[1].texto)

tests()