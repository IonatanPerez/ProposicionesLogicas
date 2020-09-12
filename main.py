class Expresion:

    name = "Expresion"
    proposiciones = {}
    mensajesError = []
    # TODO revisar bien cuando se usa el constructor que pasa porque creo que se crean expresiones que son proposiciones sin inicializar bien las variables. 
    
    def __init__(self,input,padre=False,reemplazar=False):
        if input:
            self.padre = padre
            self.operadores = [Parentesis(),SiSoloSi(),Implica(),Proposicion()]
            if reemplazar:
                if type(input) == str:
                    for operador in self.operadores:
                        input = operador.reemplazarCaracteres(input)        
            if type(input) == str:
                self.texto = input
                self.elementos = []
            else:
                self.texto = self.expresiontotext(input)
                self.elementos = []
                # self.recuperarProposiciones (input) Creo que habria que ejecutarlo despues de validar. Todavia no empece a implementar esta parte 
                # self.recuperarErrores (input) Creo que no hace falta
            self.validado = False
            self.continuarValidacion = True
            self.validar()
        else:
            if padre:
                error = MensajeError(padre,self,"Se esta intentando crear una expresion proposicional sin contenido")
                padre.mensajesError.append(error)

    def create(self,input,padre=False,reemplazar=False):
        if len(input) == 1:
            if not type(input[0]) == str:
                if input[0].name == Expresion.name:
                    return input[0]
        return Expresion(input,padre,reemplazar)

    def validar(self):
        for operador in self.operadores:
            if self.continuarValidacion:
                if operador.name == Parentesis.name:
                    operador.aplicarOperador(self)
                elif operador.name == Proposicion.name:
                    operador.aplicarOperador(self)
                else:
                    if not self.texto.find(operador.simbolo) == -1:
                        operador.aplicarOperador(self)
        if len(self.mensajesError):
            for error in self.mensajesError:
                print (error.reportar())
        else:
            self.validado = True

    def totext(self):
        if len(self.elementos) == 1:
            assert self.elementos[0].name == Proposicion.name, "hay un solo elemento en la expresión y no es una proposicion" 
            return self.elementos[0].totext()
        else:
            texto = "("
            for elemento in self.elementos:
                texto = texto + elemento.totext()
            texto = texto + ")"
            return texto

        return " (" + self.texto + ") "

    def expresiontotext(self,input):
        # TODO pensar si tiene sentido validar que solo haya elementos str, expresiones o proposiciones. No, no tiene sentido porque esto procesa el input, no el contenido. 
        texto = ""
        for elemento in input:
            if type(elemento) == str:
                texto = texto + elemento
            else:
                texto = texto + elemento.totext()
        return texto

"""     def recuperarProposiciones (self,input):
        self.proposiciones = {}
        for elemento in input:
            if type(elemento) == Expresion:
                self.proposiciones.update(elemento.proposiciones) # TODO revisar el tema de los sets para unificar proposiciones

    def recuperarErrores (self,input):
        self.mensajesError = []
        for elemento in input:
            if type(elemento) == Expresion:
                self.mensajesError = self.mensajesError + elemento.mensajeError
 """
class MensajeError:

    def __init__(self,contexto,operacion,mensaje):
        self.contexto = contexto
        self.operacion = operacion
        self.mensaje = mensaje

    def reportar(self):
        return "En el la expresion " + self.contexto.texto + " se encontro un error al procesar un operador de tipo " + self.operacion.name + " que reporto el siguiente mensaje: " + self.mensaje

class Operador:

    name = None
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
        
        if len(aperturas) == 0: # No se encontraron parentesis
            expresion.elementos.append(expresion.texto) 
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
                        if not type(expresion.elementos[-1]) == str: #TODO Revisar si esta bien este chequeo, sobre todo el mensaje de error. Porque no tiene sentido que haya una proposicion creo. El parentesis es lo primero que se chequea a partir del texto
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
            
            if len(expresion.elementos) == 1: # Si solo hay un elemento deberia ser una expresion y no hay mas que validar
                expresion.continuarValidacion = False
            else:
                #TODO pasar el to texto a cuando se arma, tipo constructor no en el init. Hacer que solo se reciba texto
                pass
            
class Proposicion(Operador):

    equivalencias = []
    name = "Proposicion"
    prioridad = -1

    def __init__(self,texto=None):
        self.texto = texto

    def aplicarOperador(self,expresion):
        if len(expresion.elementos) > 1:
            for elemento in expresion.elementos:
                assert type(elemento) == Expresion or type(elemento) == str, "revisar porque hay un error de codigo y se genero una expresion donde se llego a evaluar las proposiciones y se heredo algo que por construccion no deberia"
            error = MensajeError(expresion,Proposicion,"En la expresion se encontro una proposicion contigua a otra proposicion o expresion proposicional sin operador valido de por medio.")
            expresion.mensajesError.append(error)
            return
        assert len(expresion.elementos) == 1, "A este punto deberia solo llegar un string en elementos"
        assert type(expresion.elementos[0]) == str, "A este punto deberia solo llegar un string en elementos"
        ## TODO hacer en parentesis que si no queda texto y hay mas de un elemento tire error
        expresion.elementos = [Proposicion(expresion.elementos[0])]
        expresion.continuarValidacion = False

    def totext(self):
        return self.texto
    
class EOE(Operador):

    name = "Operador generico que opera entre dos expresiones"
    asociativo = None
    prioridad = None
    simbolo = None
    
    def aplicarOperador(self,expresion): #TODO buscar si aparece el operador en el texto para descartar rapido cuando no esta
        idelementoDeOcurrencia = None
        ocurrencias = 0
        for idx, elemento in enumerate(expresion.elementos):
            if type(elemento) == str:
                if elemento.count(self.simbolo):
                    ocurrencias = ocurrencias + elemento.count(self.simbolo)
                    idelementoDeOcurrencia = idx
        if ocurrencias > 0:
            if not self.asociativo: 
                if ocurrencias > 1:
                    error = MensajeError(expresion,self,"Se encontro mas de una ocurrencia del operador " + self.name + "(" + self.simbolo + ")" + " en la expresion, lo cual es ambiguo respecto a cual resolver primero.")
                    expresion.mensajesError.append(error)
                    return       
            # Buscamos ver que no este mal escrita la expresion porque hay otro operador de igual prioridad incompatible sintacticamente. Por construccion no deberia existir expresiones que tengan mas de tres elementos.
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
            # Si llegamos aca toda la sintaxis deberia estar bien y deberiamos tener la expresion segmentada en tres, la expresion que viene antes del operador, el operador y lo que viene despues. 
            expresion.elementos = []
            expresion.elementos.append(expresion.create(expresionIzquierda,expresion))
            expresion.elementos.append(self)
            expresion.elementos.append(expresion.create(expresionDerecha,expresion))

    def totext(self):
        return self.simbolo

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


def tests():
    texto = "((q))"
    expresion = Expresion(texto,reemplazar=True)
    print (expresion.elementos)
    print (expresion.elementos[2].elementos)
    print (expresion.totext())
    #print (expresion.elementos[5].elementos)

tests()