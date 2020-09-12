# Documentacion

## Objetivo del código

Este codigo tiene por objetivo construir las tablas de verdad de una expresion proposicional logica. Para eso debe realizar varias tareas a partir de ciertas definiciones vinculadas a las definiciones y convenciones de la logicas matematica binaria. Por un lado debe conocer cuales son los operadores logicos convencionales como se aplican (tablas de verdad) a conjuntos de proposicones. Por otro lado debe verificar que la sintaxis de la expresion sea logicamente valida y lograr segmentar la misma en unidades que sean expresiones proposicionales valida. Por ultimo debe saber reconocer cuales son las proposiciones existentes y evaluar la expresion en todas sus combinaciones de valores de verdad posible. 

Para resolver eso se encaro el problema de un modo constructivo y recurrente mediante un codigo orientado a objetos dado que la logica con que se analiza una expresion proposicional arbitraria permite mediante recurrencia analisar una expresion arbitrariamente compleja mediante pasos sencillos y encapsulados. En el proceso de recuerrencia se identifica en cada paso la estructura de operadores fundantales y simultaneamente se detectan posibles incoherencias de sintaxis. 

## Convenciones y definiciones utilizadas

Para analizar las expresiones logicas se utilizan las siguientes definiciones y convenciones:

- Una expesion logica valida esta conformada por: proposiciones, expresiones logicas y operadores. 
- Las proposiciones tienen valores de verdad arbitrarios y estan formados basicamente por una cadena de texto donde no se puede identificar operadores y que representa un nombre arbitrario. 
- Los operadores se identifican con ciertas cadenas de texto especificas (por ej: "->", "y", ")") que indican que se debe aplicar ciertas tablas de verdad a las proposiciones que los rodean.
- Las expresiones proposicionales son conjuntos de expresiones proposicionales, proposiciones y operadores que son sintacticamente validas y que tienen un valor de verdad dado por sus componentes.

- Las proposiciones estan formadas por un texto al que se le puede asignar un valor de verdad arbitrario
- Los operadores son los que se listan a continuacion y estan definidos por su tabla de verdad, sus reglas sintacticas y sus caracteres asociados. A su vez el orden en que deben ser aplicados esta dado por su prioridad donde los operadores con prioridad positiva se deben evaluar en orden cresciente (sintacticamente se procesan en un orden para construir expresiones mas pequeñas dentro de expresiones complejas pero luego se evalua su valor de verdad en orden inverso). Se reserva la priordad -1 para las proposiciones.

## Definiciones

  - Parentesis: 
    - Prioridad = 0
    - Simbolos validos: "(" ")", "[" "]", "{" "}"
    - Simbolo default: "(" ")"
    - Reglas sintacticas: Debe contener una expresion o proposicion valida. No puede estar adyacente a otra proposicion o expresion proposicional.
    - Tabla de verdad: [VF] (para una expresion con valores de verdad VF)
  - SiSoloSi
    - Prioridad = 1
    - Simbolos validos: "<=>", "<->"
    - Simbolo default "<=>"
    - Reglas sintacticas: Debe tener una expresion o proposicion delante y detras (A esto lo llamaremos EOE). No conmuta, es decir solo puede haber uno por expresion.
    - Tabla de verdad: [VFFV] (Para expresiones que cumplan con ser en orden izq-der VV ,VF, FV, FF)
  - Implica
    - Prioridad = 2
    - Simbolos validos: "->", "=>"
    - Simbolo default "=>"
    - Reglas sintacticas: EOE, No conmuta.
    - Tabla de verdad: [VFVV]
  - Y
    - Prioridad = 3
    - Simbolos validos: "Y", "y", "^", "&", "AND", "and"
    - Simbolo default: "y"
    - Reglas sintacticas: EOE, conmuta (puede haber mas de un operador del mismo tipo pero no de otro tipo con la misma prioridad). En caso de que haya mas de uno en una expresion, es arbitrario cual se aplica primero por lo que al separar la expresion en la forma: "Expresion - Operador - Expresion" los demas operadores del mismo tipo quedaran dentro de algunas de las expresiones generadas.
    - Tabla de verdad: [VFFF]
  - O
    - Prioridad = 3
    - Simbolos validos: "O", "o", "v", "V", "+", "or", "OR" 
    - Simbolo default "o"
    - Reglas sintacticas: EOE, conmuta.
    - Tabla de verdad: [VVVF] 
  - OExcluyente
    - Prioridad = 3
    - Simbolos validos: "Ó", "ó", "xor", "XOR"
    - Simbolo default "ó"
    - Reglas sintacticas: EOE, conmuta.
    - Tabla de verdad: [FVVF]
  - Negacion
    - Prioridad = 4
    - Simbolos validos: "!", "~", "¬", "not", "NOT"
    - Simbolo default: "!"
    - Reglas sintacticas: Debe iniciar una expresion y estar seguido por una expresion o proposicion
    - Tabla de verdad: [FV]

## Logica de programación

Para resolver el problema se sigue la siguiente logica:

### Segmentación (en proceso de implementacion)

- Se define las expresiones como un objeto que poseen (ademas de variables y metodos auxiliares) las siguientes caracteristicas:
  - Propiedad texto: es el texto de la expresion que debe ser validado
  - Propiedad elementosTemporales: son las componentes temporales de la expresion que al crearse se iran validando. 
  - Propiedad expresiones: es un conjunto de a lo sumo dos expresiones entre las cuales se debe realizar la operacion.
  - Propiedad operacion: es el operador que se debe realizar entre las expresiones asumiendo que se haya pasado el proceso de validacion. 
  - Metodo validar: 
    - Se ejecuta al crear la expresion. Toma al texto, lo segmenta y procesa segun corresponda a los operadores mencionados arriba en el orden correcto. 
    - Al aplicar cada operador se valida la sintaxis y si no se cumple se genera el error explicativo correspondiente. 
    - Si un operador es aplicado con exito es porque la sintaxis evaluada en ese nivel de anidacion es correcta (excepto para el caso Parentesis). 
    - Luego de aplicar todos los operadores no deberia quedar texto a transformar en elemento ni posibles errores de sintaxis sin validar. 
    - Como la logica del codigo es toda orientada a objetos si hay un error sintactico en una expresion anidada eso es un problema que se valua cuando un operador crea la expresion anidada a partir del segmento de texto que corresponda. 
    - Como se genera una cadena de validaciones anidadas si el proceso no genera errores quiere decir que en ningun lugar de la expresion hay errores sintacticos.
    -  Si la validacion se interrumpe porque se encuentra un error este error se reporta al usuario indicando razon y contexto del error. 
- Se definen la clase Operador como clases que tienen un metodo de reemplazar caracteres.
- Se define el operado parentesis como clase hija de Operador. 
  - Es el primer operador que se debe aplicar y toma el texto de la expresion para hacer la primer segmentación. 
  - Luego de aplicado la expresion tiene en sus elementos temporales textos y expresiones que corresponden a el o los parentesis de mas alto nivel. Salvo que solo haya un parentesis en cuyo caso significa que el parentesis era irrelevante y simplemente se deja el contenido del mismo para que sea procesado por los operadores subsiguientes. 
  - Deberia surgir un error si hay dos parentesis consecutivos, pero podemos limitarnos a elevar error solo si no queda texto remanente ya que eso implica que hay dos o mas expresiones (si era una ya lo consideramos antes) sin operacion para combinarlas. En caso de que haya dos expresiones consecutivas pero haya texto el texto deberia ser procesado por algun operador que va a validar el problema mas adelante. 
- Se define los operadores del tipo EOE como hijos de Operador
  - Se hace una clase generica porque se valida siempre igual al margen del tipo de operador especifico que se trate. Las diferencias se definen mediante clases heredadas. 
  - Este operador aplica buscando en lo que quede de texto (es decir lo que no este entre parentesis que ya fue procesado por el operador anterior) el simbolo que corresponda a su clase hija especifica. 
  - Cuando lo encuentra verifica que este simbolo sea unico salvo que conmute (en cuyo caso verifica que no haya un simbolo de otro operador diferente con el mismo orden de prioridad). 
  - A continuacion segmenta toda la expresion en tres, lo que esta a la izquierda (que sera una expresion nueva), el operador y lo que esta a la izquierda (que sera otra expresion nueva). Si encuentra que alguna de las condiciones no se cumple eleva un error, sino mueve las expresiones a la propiedad expresiones de la expresion actual y se establece como el operador que corresponde a la expresion activa. Al quedar liberado de elementos la propiedad elementosTemporales se finaliza la validacion de la expresion activa. 
  - Esta clase da errro si no logra encontrar elementos a izquierda y derecha del caracter que rempresenta al operador. 
- Se define el operador negación como clase hija de Operador.
  -  Es el unico que opera solo con una expresion a la derecha. 
  -  Busca en lo que sea texto el simbolo correspondiente, debe ser el primer caracter y tener algo a continuacion  
- Se define el operador Proposicion. Se ejecuta si queda texto luego de buscar los elementos que caracterizar a cualquier otro operador.
  -  Solo tiene sentido que haya un unico elemento de texto si se llega esta instancia, sino se eleva un error. 


#### Algunas elecciones y aclaraciones tecnicas

- Las clases Expresion, Proposicion y MensajeError deberian ser instanciables, las clases que corresponden a operadores no, vamos a ver como sale. 
- En la logica de deteccion de inconsistencias semanticas hay algo con lo que hay que tener cuidado porque hay dos clases que generan expresiones, la primera en validarse (Parentesis) y la ultima (Proposiciones), y la validacion debe ser consistente. 
  - Si hacemos que Parentesis verifique que no queden dos expresiones creadas con parentesis consecutivas (cosa que no puede suceder) y nada mas todavia podria pasar que el texto fuera del parentesis incluya o sea una proposcion que vaya a quedar consecutiva al parentesis. El problema es que eso no puede ser validado por Parentesis. 
  - Luego se validan todos los operadores de la forma EOE o OE (Negacion) pero estos operadores toman todo lo que haya en la expresion a validar antes y despues del operador conviertiendo cada parte en una expresion que se validara un nivel mas abajo por lo que solucionan el problema. La cuestion es estudiar que pasa si no aparece ningun otro operador en lo que queda de texto luego de aplicar parentesis. 
  - En este ultimo caso llegariamos a aplicar el operador proposicion a una expresion que tiene mas de un elemento (lo que venia del parentesis y el texto remanente)

### Busqueda de proposiciones (pendiente)

Una vez segmentada y validada la expresion la idea es recorrela para buscar en los diferentes niveles de anidacion todos los objetos de tipo Proposicion y unificarlos conviertiendo en una misma instancia de la clase las proposiciones cuyos texto coincidan. Ademas se debe generar la combinacion de valores de verdad de dichas proposiciones para poder evaluar luego las expresiones. Hay que agregar el metodo (posiblemente a nivel EOE y negacion) que calcule la tabla de verdad de la expresion. Hay que ver si conviene crear a priori todas las combinaciones posibles de valor de verdad de las proposiciones o conviene crear un metodo de evaluacion para que despues seteando los valores automaticamente se updatee los valore de cada expresion.

### Representacion grafica (pendiente)

En principio la solucion facil es crear tablas pandas y trabajarlo con una visualizacion tipica de dataframes donde cada fila es una combinacion de valor de verdad de las proposiciones y cada columna cada una de las expresiones anidadas (habria que ordenarlas en orden de menor a mayor complejidad). Despue se puede pensar en hacer una interfaz grafica mas copada. 
