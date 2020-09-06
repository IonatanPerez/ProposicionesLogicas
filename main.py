class Expresion:

    name = "Expresion"

    def __init__(self,input,padre=False,reemplazar=False):
        if input:
            self.padre = padre
            self.operadores = [Parentesis(),SiSoloSi(),Proposicion()]
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
        if len(self.elementos) == 1:
            assert self.elementos[0].name == self.operadores[-1].name
            return self.elementos[0].totext()
        else:
            texto = "("
            for elemento in elementos:
                texto = texto + elemento.totext()
            texto = texto + ")"
            return texto

        return " (" + self.texto + ") "

    def expresiontotext(self,input):
        # TODO pensar si tiene sentido validar que solo haya elementos str, expresiones o proposiciones
        texto = ""
        for elemento in input:
            if type(elemento) == str:
                texto = texto + elemento
            else:
                texto = texto + elemento.totext()
        return texto

    def recuperarProposiciones (self,input):
        self.proposiciones = {}
        for elemento in input:
            if type(elemento) == Expresion:
                self.proposiciones.update(elemento.proposiciones) # TODO revisar el tema de los sets para unificar proposiciones

    def recuperarErrores (self,input):
        self.mensajesError = []
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

    name = None
    equivalencias = None

    def reemplazarCaracteres(self,texto):
        for subtipo in self.equivalencias:
            for char in subtipo[1:]:
                texto = texto.replace(char,subtipo[0])
        return texto


class Parentesis(Operador):
    equivalencias = [["(","[","{"],[")","]","}"]]
    prioridad = 0
    name = "Parentesis"

    simboloApertura = equivalencias[0][0]
    simboloCierre = equivalencias[1][0]

    def aplicarOperador (self,expresion):

        aperturas = []
        apertura = -1
        while expresion.texto[apertura+1:].find(self.simboloApertura) != -1:
            if aperturas:
                offset = aperturas[-1]+1
            else:
                offset = 0
            apertura = expresion.texto[apertura+1:].find(self.simboloApertura) + offset
            aperturas = aperturas + [apertura]

        cierres = []
        cierre = -1
        while expresion.texto[cierre+1:].find(self.simboloCierre) != -1:
            if cierres:
                offset = cierres[-1]+1
            else:
                offset = 0
            cierre = expresion.texto[cierre+1:].find(self.simboloCierre) + offset
            cierres = cierres + [cierre]

        if len(aperturas) != len(cierres):
            error = MensajeError(expresion,Parentesis,"En la expresion se encontro una cantidad diferente de parentesis de apertura que de cierre.")
            expresion.mensajesError.append(error)
            return
        
        if len(aperturas) == 0:
            expresion.elementos.append(expresion.texto) # TODO Aca es la segunda vez que lo cambio, va esto para transformar el texto en elemento. 
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
                    expresion.elementos.append(Expresion(contenido,expresion))
                else:
                    error = MensajeError(expresion,Parentesis,"En la expresion se encontro un parentesis de apertura y cierre sin contenido.")
                    expresion.mensajesError.append(error)
                    return
                remanente = expresion.texto[par[1]+1:]
            if remanente:
                expresion.elementos.append(remanente)


class Proposicion(Operador):

    equivalencias = []
    name = "Proposicion"
    prioridad = -1

    def __init__(self,texto=None):
        self.texto = texto

    def aplicarOperador(self,expresion):
        for idx, elemento in enumerate(expresion.elementos):
            if type(elemento) == str:
                if idx>1:
                    if expresion.elementos[idx-1].name == "Expresion":
                        error = MensajeError(expresion,Proposicion,"En la expresion se encontro una proposicion a continuacion de una expresion proposicional sin operador de por medio valido.")
                        expresion.mensajesError.append(error)
                        return
                    if expresion.elementos[idx-1].name == "Proposicion":
                        error = MensajeError(expresion,Proposicion,"En la expresion se encontro una proposicion a continuacion de una proposicion sin operador de por medio valido.")
                        expresion.mensajesError.append(error)
                        return
                if idx + 1 < len(expresion.elementos):
                    if expresion.elementos[idx+1].name == "Expresion":
                        error = MensajeError(expresion,Proposicion,"En la expresion se encontro una proposicion justo antes de una expresion proposicional sin operador de por medio valido.")
                        expresion.mensajesError.append(error)
                        return
                expresion.elementos[idx] = Proposicion(elemento)


class EOE(Operador):

    name = "Operador generico que opera entre dos expresiones"
    asociativo = None
    prioridad = None
    
    def aplicarOperador(self,expresion):
        idelementoDeOcurrencia = None
        ocurrencias = 0
        for idx, elemento in enumerate(expresion.elementos):
            if type(elemento) == str:
                if elemento.count(self.simbolo):
                    ocurrencias = ocurrencias + elemento.count(self.simbolo)
                    idelementoDeOcurrencia = idx
        if ocurrencias > 0:
            # Buscamos ver que no este mal escrita la expresion porque hay otro operador de igual prioridad incompatible sintacticamente. 
            # TODO Pensar si tiene sentido chequear que no hayan quedado operadores de mas prioridad.
            for elemento in expresion.elementos:
                if type(elemento) == str:
                    for operador in expresion.operadores:
                        if operador.prioridad == self.prioridad:
                            if not operador.name == self.name: 
                                if elemento.find(operador.simbolo):
                                    error = MensajeError(expresion,self,"Se encontro una ocurrencia del operador " + self.name + "(" + self.simbolo + ")" + " en la expresion al mismo nivel que una del tipo " + 
                                                operador.name + "(" + operador.simbolo + ")" + ". Es ambiguo cual resolver primero.")
                                    expresion.mensajesError.append(error)
                                    return      
            if not self.asociativo:
                if ocurrencias > 1:
                    error = MensajeError(expresion,self,"Se encontro mas de una ocurrencia del operador " + self.name + "(" + self.simbolo + ")" + " en la expresion, lo cual es ambiguo respecto a cual resolver primero.")
                    expresion.mensajesError.append(error)
                    return       
            caracterOcurrencia = expresion.elementos[idelementoDeOcurrencia].find(self.simbolo)
            pre = expresion.elementos[idelementoDeOcurrencia][:caracterOcurrencia]
            post = expresion.elementos[idelementoDeOcurrencia][caracterOcurrencia+len(self.simbolo):]
            if pre:
                expresionIzquierda = expresion.elementos[:idelementoDeOcurrencia] + [pre]
            else:
                expresionIzquierda = expresion.elementos[:idelementoDeOcurrencia]
            if post:
                expresionDerecha = [post] + expresion.elementos[idelementoDeOcurrencia+1:]
            else:
                expresionDerecha = expresion.elementos[idelementoDeOcurrencia+1:]
            if not expresionIzquierda:
                error = MensajeError(expresion,self,"No se encontró una expresion valida delante del operador.")
                expresion.mensajesError.append(error)
                return
            if not expresionDerecha:
                error = MensajeError(expresion,self,"No se encontró una expresion valida detras del operador.")
                expresion.mensajesError.append(error)
                return
            # Si llegamos aca toda la sintaxis deberia estar bien
            expresion.elementos = []
            expresion.elementos.append(Expresion(expresionIzquierda,expresion))
            expresion.elementos.append(self)
            expresion.elementos.append(Expresion(expresionDerecha,expresion))


class SiSoloSi (EOE):

    name = "SiSoloSi"
    equivalencias = [["<=>","<->"]]
    asociativo = False
    simbolo = equivalencias[0][0]
    prioridad = 1


def tests():
    texto = "p<->(q)"
    expresion = Expresion(texto,reemplazar=True)
    print (expresion.elementos)
    print (expresion.elementos[0].elementos)
    #print (expresion.elementos[5].elementos)

tests()