# Documentacion

## Objetivo del código

Este codigo tiene por objetivo construir las tablas de verdad de una expresion proposicional logica. Para eso debe realizar varias tareas a partir de ciertas definiciones vinculadas a las definiciones y convenciones de la logicas matematica binaria. Por un lado debe conocer cuales son los operadores logicos convencionales como se aplican (tablas de verdad) a conjuntos de proposicones. Por otro lado debe verificar que la sintaxis de la expresion sea logicamente valida y lograr segmentar la misma en unidades que sean expresiones proposicionales valida. Por ultimo debe saber reconocer cuales son las proposiciones existentes y evaluar la expresion en todas sus combinaciones de valores de verdad posible. 

Para resolver eso se encaro el problema de un modo constructivo y recurrente mediante un codigo orientado a objetos dado que la logica con que se analiza una expresion proposicional arbitraria permite mediante recurrencia analisar una expresion arbitrariamente compleja mediante pasos sencillos y encapsulados. En el proceso de recuerrencia se identifica en cada paso la estructura de operadores fundantales y simultaneamente se detectan posibles incoherencias de sintaxis. 

## Convenciones y definiciones utilizadas

Para analizar las expresiones logicas se utilizan las siguientes definiciones y convenciones:

- Una expesion logica valida esta conformada por: proposiciones, expresiones logicas u operadores. 
- Las proposiciones tienen valores de verdad arbitrarios y estan formados basicamente por una cadena de texto donde no se puede identificar operadores y que representa un nombre arbitrario. 
- Los operadores se identifican con ciertas cadenas de texto especificas (por ej: "->", "y", ")") que indican que se debe aplicar ciertas tablas de verdad a las propociociones que los rodean.
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
  - Propiedad elementos: son las componentes de la expresion que al crearse se iran validando. 
  - Metodo validar: Se ejecuta al crear la expresion. Toma al texto y lo segmenta y procesa segun corresponda a los operadores mencionados arriba en el orden correcto. Al aplicar cada operador se valida la sintaxis y si no se cumple se genera el error explicativo correspondiente. Si un operador es aplicado con exito es porque la sintaxis evaluada en ese nivel de anidacion es correcta. Luego de aplicar todos los operadores no deberia quedar texto a transformar en elemento ni posibles errores de sintaxis sin validar. Como la logica del codigo es toda orientada a objetos si hay un error sintactico en una expresion anidada eso es un problema que se valua cuando un operador crea la expresion anidada a partir del segmento de texto que corresponda. Como se genera una cadena de validaciones anidadas si el proceso no genera errores quiere decir que en ningun lugar de la expresion hay errores sintacticos. Si la validacion se interrumpe porque se encuentra un error este error se reporta al usuario indicando razon y contexto del error. 
- Se definen la clase Operador como clases que tienen un metodo de reemplazar caracteres (para poder unificar los caracteres diferentes con una logica unica)
- Se define el operado parentesis como clase hija de Operador. Es el primer operador que se debe aplicar y toma el texto de la expresion para hacer la primer segmentacion. Luego de aplicado la expresion tiene en sus elementos textos y (si corresponde porque se encontraron parentesis) tambien expresiones. Si el operador detecta que no hay mas texto a analizar lo indica para evitar revisiones posteriores de otros operadores de prioridad mas baja. Lo mismo hacen todos los operadores. 
- Se define los operadores del tipo EOE como hijos de Operador, porque su logica de validacion es muy similar al margen del tipo de operador especifico que sea cuyas diferencias se definen mediante clases heredadas. Este operador aplica buscando en lo que quede de texto (es decir lo que no este entre parentesis que ya fue procesado por el operador anterior) el simbolo que corresponda a su clase hija especifica. Cuando lo encuentra verifica que este simbolo sea unico salvo que conmute (en cuyo caso verifica que no haya un simbolo de otro operador diferente con el mismo orden de prioridad). A continuacion segmenta toda la expresion en tres, lo que esta a la izquierda (que sera una expresion nueva), el operador y lo que esta a la izquierda (que sera otra expresion nueva). Si encuentra que alguna de las condiciones no se cumple eleva un error, sino marca como finalizada la validacion de la expresion. 
- Se define el operador negación como clase hija de Operador. Es el unico que opera solo con una expresion a la derecha. Busca en lo que sea texto el simbolo correspondiente, debe ser el primer caracter y lo que sigue debe ser todo texto o bien una expresion ya creada (por un parentesis). 
- Se define el operador Proposicion. Se ejecuta si queda texto luego de buscar los elementos que caracterizar a cualquier otro operador. Solo tiene sentido que haya un unico elemento de texto si se llega esta instancia, sino se eleva un error. Se reemplaza el texto por un objeto que contiene al texto pero es una proposicion. 

### Busqueda de proposiciones (pendiente)

Una vez segmentada y validada la expresion la idea es recorrela para buscar en los diferentes niveles de anidacion todos los objetos de tipo Proposicion y unificarlos conviertiendo en una misma instancia de la clase las proposiciones cuyos texto coincidan. Ademas se debe generar la combinacion de valores de verdad de dichas proposiciones para poder evaluar luego las expresiones. Hay que agregar el metodo (posiblemente a nivel EOE y negacion) que calcule la tabla de verdad de la expresion. Hay que ver si conviene crear a priori todas las combinaciones posibles de valor de verdad de las proposiciones o conviene crear un metodo de evaluacion para que despues seteando los valores automaticamente se updatee los valore de cada expresion.

### Representacion grafica (pendiente)

En principio la solucion facil es crear tablas pandas y trabajarlo con una visualizacion tipica de dataframes donde cada fila es una combinacion de valor de verdad de las proposiciones y cada columna cada una de las expresiones anidadas (habria que ordenarlas en orden de menor a mayor complejidad). Despue se puede pensar en hacer una interfaz grafica mas copada. 
