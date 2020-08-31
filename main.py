# TODO Revisar que no haya dos expresiones consecutivas

class Expresion:
            
    def __init__(self,input,reemplazar=False):
        self.operadores = [Parentesis()]
        if reemplazar:
            if type(input) == str:
                for operador in self.operadores:
                    input = operador.reemplazarCaracteres(input)        
        if type(input) == str:
            self.texto = input
            self.elementos = []
            self.proposiciones = {}
            self.mensajesError = []
        else:
            self.texto = self.expresiontotext(input)
            self.elementos = []
            self.recuperarProposiciones (input)
            self.recuperarErrores (input)
        self.validado = False
        self.validar()

    def validar(self):
        for operador in self.operadores:
            # self.texto = operador.reemplazarCaracteres(self.texto)         # No me queda claro porque en algun momento hice esto aca
            operador.aplicarOperador(self)
        if len(self.mensajesError):
            for error in self.mensajesError:
                print (error.reportar())
        else:
            self.validado = True

    def totext(self):
        return " (" + self.texto + ") "

    def expresiontotext(self,input):
        texto = ""
        for elemento in input:
            if type(elemento) == str:
                texto = texto + elemento
            else:
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

class MensajeError:

    def __init__(self,contexto,operacion,mensaje):
        self.contexto = contexto
        self.operacion = operacion
        self.mensaje = mensaje

    def reportar(self):
        return "En el la expresion " + self.contexto.texto + " se encontro un error al procesar un operador de tipo " + self.operacion.name + " que reporto el siguiente mensaje: " + self.mensaje

class Operador:

    #name = "por definir"
    #equivalencias = []

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

        aperturas = []
        apertura = -1
        while expresion.texto[apertura+1:].find(self.equivalencias[0][0]) != -1:
            if sum(aperturas):
                offset = sum(aperturas,1)
            else:
                offset = 0
            apertura = expresion.texto[apertura+1:].find(self.equivalencias[0][0]) + offset
            aperturas = aperturas + [apertura]

        cierres = []
        cierre = -1
        while expresion.texto[cierre+1:].find(self.equivalencias[1][0]) != -1:
            if sum(cierres):
                offset = sum(cierres,1)
            else:
                offset = 0
            cierre = expresion.texto[cierre+1:].find(self.equivalencias[1][0]) + offset
            cierres = cierres + [cierre]

        if len(aperturas) != len(cierres):
            error = MensajeError(expresion,Parentesis,"En la expresion se encontro una cantidad diferente de parentesis de apertura que de cierre.")
            expresion.mensajesError.append(error)
            return
        
        if len(aperturas) == 0:
            expresion.elementos = expresion.texto
        else:
            pares = []
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
                    error = MensajeError(expresion,Parentesis,"En la expresion se encontro un parentesis de apertura antes que uno de cierre.")
                    expresion.mensajesError.append(error)
                    return
            remanente = expresion.texto
            for par in pares:
                expresion.elementos.append(expresion.texto[len(expresion.texto)-len(remanente):par[0]])
                expresion.elementos.append(Expresion (expresion.texto[par[0]+1:par[1]]))
                remanente = expresion.texto[par[1]+1:]
            expresion.elementos.append(remanente)

        
        """
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
        """
        
class SiSoloSi(Operador):

    equivalencias = [["<=>","<->"]]
    prioridad = 1
    name = "SiSoloSi"

    def aplicarOperador(self,expresion):
        elementosNuevo = []

class Proposicion:

    # TODO transformar en un operador que verifique que no haya dos proposiciones seguidas.
    def __init__(self,texto):
        self.texto = texto

def tests():
    texto = "H(ol)(hay)a"
    expresion = Expresion(texto,reemplazar=True)
    print (expresion.elementos)
    print (expresion.elementos[1].elementos)
    print (expresion.elementos[3].elementos)
tests()