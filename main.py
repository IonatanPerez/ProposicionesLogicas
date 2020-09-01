# TODO Revisar que no haya dos expresiones consecutivas

class Expresion:

    name = "Expresion"

    def __init__(self,input,padre=False,reemplazar=False):
        if input:
            self.padre = padre
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
        else:
            if padre:
                error = MensajeError(padre,self,"Se esta intentando crear una expresion proposicional sin contenido")
                padre.mensajesError.append(error)

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

        aperturas = []
        apertura = -1
        while expresion.texto[apertura+1:].find(self.equivalencias[0][0]) != -1:
            if aperturas:
                offset = aperturas[-1]+1
            else:
                offset = 0
            apertura = expresion.texto[apertura+1:].find(self.equivalencias[0][0]) + offset
            aperturas = aperturas + [apertura]

        cierres = []
        cierre = -1
        while expresion.texto[cierre+1:].find(self.equivalencias[1][0]) != -1:
            if cierres:
                offset = cierres[-1]+1
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
                pre = expresion.texto[len(expresion.texto)-len(remanente):par[0]]
                if pre:
                    expresion.elementos.append(expresion.texto[len(expresion.texto)-len(remanente):par[0]])
                contenido = expresion.texto[par[0]+1:par[1]]
                if contenido:
                    if expresion.elementos:
                        if not type(expresion.elementos[-1]) == str:
                            if expresion.elementos[-1].name == Expresion.name:
                                error = MensajeError(expresion,Parentesis,"En la expresion se encontro un parentesis consecutivo a otro o consecutivo a una expresion proposicional sin operador de por medio.")
                                expresion.mensajesError.append(error)
                                return    
                    expresion.elementos.append(Expresion(expresion.texto[par[0]+1:par[1]],expresion))
                else:
                    error = MensajeError(expresion,Parentesis,"En la expresion se encontro un parentesis de apertura y cierre sin contenido.")
                    expresion.mensajesError.append(error)
                    return
                remanente = expresion.texto[par[1]+1:]
            if remanente:
                expresion.elementos.append(remanente)


class SiSoloSi(Operador):

    equivalencias = [["<=>","<->"]]
    prioridad = 1
    name = "SiSoloSi"

    def aplicarOperador(self,expresion):
        elementosNuevo = []


class Proposicion:

    # TODO transformar en un operador que verifique que no haya dos proposiciones seguidas, ni una proposicion consecutiva a una exoresion
    name = "Proposicion"

    def __init__(self,texto):
        self.texto = texto

    def aplicarOperador(self,expresion):
        for idx, elemento in enumerate(expresion.elementos):
            if type(elemento) == str:
                if idx>1:
                    pass
                expresion.elementos[idx] = Proposicion(elemento)




def tests():
    texto = "H(ol)y(hay)o((q)a)a"
    expresion = Expresion(texto,reemplazar=True)
    print (expresion.elementos)
    print (expresion.elementos[1].elementos)
    print (expresion.elementos[5].elementos)

tests()