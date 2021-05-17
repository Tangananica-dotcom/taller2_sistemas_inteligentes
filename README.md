# taller2_sistemas_inteligentes

Alumnos: Pedro Catrilef – Carlos Contreras

La administración nacional de aeronáutica y espacio (NASA), ha encargado construir una aplicación que permita controlar los movimientos del robot SPIRIT, encargado de explorar la superficie marciana. La superficie marciana puede considerarse como una matriz de n × m metros, donde cada cuadrante es de 1 [mt] × 1 [mt]. Ver Figura 1, donde se muestra un ejemplo.

Figura 1

Cada localización L del SPIRIT viene dada por las coordenadas (i, j) del cuadrante donde se encuentra, junto con su orientación: Norte, Sur, Este, Oeste. Ejemplo: en la Figura 1su localización es ((1,1), Este).

OBJETIVO: trasladar el SPIRIT al lugar marcado como objetivo en el menor tiempo posible partiendo desde cualquier punto de origen.
En cada momento el SPIRIT puede:
 Desplazarse en el sentido de su orientación actual al siguiente cuadrante.
 Girar sobre sí mismo 90 grados en un sentido u otro, manteniéndose en las mismas coordenadas.
Además se sabe que:

 Tarda 4 [s] en dar un giro sobre sí mismo (90 grados).
 Se desplaza a 0,5 [m/s] en terreno abrupto.
 Se desplaza a 1,2 [m/s] en terreno llano.
 No puede pasar sobre los obstáculos.

Debe asignar aleatoriamente los obstáculos, los tipos de terreno, el objetivo y la posición del robot.

Se pide:
1) Formalizar el problema de trasladar el SPIRIT desde una localización a otra en el mínimo tiempo posible, como un problema de búsqueda en espacio de estados.
2) Proponer una heurística apropiada para resolver el problema, para la implementación con búsqueda informada. Con la heurística definida se debe implementar el algoritmo de búsqueda heurística Best First de manera de encontrar y desplegar la ruta del SPIRIT.
3) Correr el algoritmo para distintos valores de n y m, analizando lo que sucede con el algoritmo.