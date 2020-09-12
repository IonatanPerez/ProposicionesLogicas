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