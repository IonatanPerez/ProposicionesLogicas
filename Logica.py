
class Expresion:

    name = "Expresion"
    operadores = [Parentesis] #, SiSoloSi, Implica, Proposicion]

    def __init__ (self,texto,padre):
        assert texto
        assert type(texto) == str
        self.texto = texto
        self.padre = padre
        self.elementosTemporales = [texto]
        self.textoRemanente = texto
        self.mensajesError = []
        self.operacion = None
        self.subexpresiones = None
        self.validado = False
        self.procesar()
        if self.mensajesError:
            for mensaje in self.mensajesError:
                mensaje.reportar()
        
    def crearsubexpresion (cls,elementosTemporales,padre):
        "Transforma un subconjunto de elementos a medio procesar en el texto correspodiente para crear una subexpresion nueva."
        texto = cls.elementosAtexto (elementosTemporales)
        assert texto
        return Expresion(texto,padre)

    def reemplazarCaracteres (cls,texto):
        "Reemplaza los caracteres de un texto asumiento que el texto fue ingresado por el usuario y hay diferentes equivalencias para los mismos simbolos"
        for operador in cls.operadores:
            texto = operador.reemplazarCaracteres(texto)
        return texto

    def expresionInicial (cls,texto):
        "Es el punto de entreda al codigo, toma el texto del usuario e inicia el proceso."
        texto = cls.reemplazarCaracteres(texto)
        expresion = Expresion(texto,False)
        if expresion.validado:
            print ("La expresion: " + expresion.texto + " ha pasado el proceso de procesamiento y validacion sintactica")
        else:
            print ("La expresion: " + expresion.texto + " no ha pasado el proceso de procesamiento y validacion sintactica")

    def totext(self):
        pass # No me queda claro para que la querria. 
        
    def procesar(self):
        pass # Revisar implementacion cuando termine de reescribir los demas elementos. 
        
class MensajeError:
    "Clase que se crea cuando aparece un error en una expresión para explicarlo."
    def __init__(self,contexto,operador,mensaje):
        self.contexto = contexto
        self.operador = operador
        self.mensaje = mensaje

    def reportar(self):
        "Genera el texto que explica el error."
        return "En el la expresion " + self.contexto.texto + " se encontro un error al procesar un operador de tipo " + self.operador.name + " que reporto el siguiente mensaje: " + self.mensaje


class Operador:
    "Clase correspondiente a un operador generico donde se definen las funciones comunes a todos."
    name = None
    equivalencias = []
    simbolo = None

    @staticmethod
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

    @staticmethod
    def buscarPares(cls,expresion):
        "Busca las posiciones de los pares de parentesis o un -1 si hay error sintactico."
        aperturas = []
        apertura = -1
        while expresion.texto[apertura+1:].find(cls.simboloApertura) != -1:
            if aperturas:
                offset = aperturas[-1]+1
            else:
                offset = 0
            apertura = expresion.texto[apertura+1:].find(cls.simboloApertura) + offset
            aperturas = aperturas + [apertura]

        cierres = []
        cierre = -1
        while expresion.texto[cierre+1:].find(cls.simboloCierre) != -1:
            if cierres:
                offset = cierres[-1]+1
            else:
                offset = 0
            cierre = expresion.texto[cierre+1:].find(cls.simboloCierre) + offset
            cierres = cierres + [cierre]

        if len(aperturas) != len(cierres):
            error = MensajeError(expresion,Parentesis,"En la expresion se encontro una cantidad diferente de parentesis de apertura que de cierre.")
            expresion.mensajesError.append(error)
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
                    error = MensajeError(expresion,Parentesis,"En la expresion se encontro un parentesis de apertura antes que uno de cierre.")
                    expresion.mensajesError.append(error)
                    return -1
        return pares

    @staticmethod
    def aplicarOperador (cls,expresion):
        """Aplica el operador parentesis a una expresion, asume que es el primer operador aplicado.

        La funcion toma el texto de la expresion y lo segmenta en funcion de los parentesis mas externos que encuentre colocando
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
        if pares == -1:
            return
        else:
            if pares:
            else:
                expresion.ele

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
