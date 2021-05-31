import numpy as np
from SPIRIT import SPIRIT
from map_gen import map_gen
import sys

from random import randrange
from Node import Node
import random
import pandas as pd

import time
import datetime
    
np.set_printoptions(threshold=sys.maxsize)
# Esta clase representa un nodo


# Algoritmo Best-first
def best_first_search(map, start, end, sprt):
    
    # Cree listas para nodos abiertos y nodos cerrados
    clear = [] #lista clear
    closed = [] #lista closed
    
    # Crea un nodo de inicio y un nodo objetivo
    start_node = Node(start, None)
    goal_node = Node(end, None)
    
    # Para comenzar, agregamos el nodo de inicio a la lista clear
    clear.append(start_node)
    
    # Loop hasta que la lista abierta (lista clear) esté vacía
    while len(clear) > 0:
        
        # Sort a la lista abierta para obtener primero el nodo con el costo más bajo
        clear.sort()
        
        # Obtener el nodo con el menor costo
        current_node = clear.pop(0)
        # Agregar el nodo actual a la lista cerrada (lista closed)
        closed.append(current_node)
        # sprt.commit(current_node.type, current_node.orientation)
        # Comprobar si se a llegado a la meta, retorna el camino (retorna path)

        # Obtener la posición actual del nodo
        if current_node == goal_node:
            sprt.commit(type = current_node.type, o = current_node.orientation, next = current_node.position)
            return sprt

        if current_node != start_node:
            sprt.commit(type = current_node.type, o=current_node.orientation, next = current_node.position)
        
        (x, y) = current_node.position
        # Obtener los vecinos del nodo
        neighbors = [[(x-1, y), "N"], [(x+1, y), "S"], [(x, y-1), "O"], [(x, y+1), "E"]]
        # Loop a los vecinos del nodo

        for next in neighbors:
            pos = next[0]
            orientation = next[1]
            if(pos <(0,0)  or pos >= tuple(np.shape(map))):
                continue
            
            # Obtener el tipo de terreno (value)
            # Si se sale de la lista es porque es una pared
            try:
                map_value = map[pos]
            except IndexError:
                map_value = 2
            
            # Con el value, comprobar si el nodo es una pared (obstaculo).
            if(map_value == 2):
                continue
            
            # Si no es una pared, entonces es valido y creamos un nodo vecino
            neighbor = Node( pos, current_node, o=orientation, value=map_value)
            
            # Comprobar si el nodo vecino está en la lista cerrada
            if(neighbor in closed):
                continue
            
            # Si no esta en la lista cerrada, entonces es un nodo valido, y generamos la heurística
            # (distancia al nodo destino)
            neighbor.h = (abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1]))**2 + map_value + sprt.weight_turn(orientation)
            
            # Comprobar si el nodo vecino está en la lista abierta
            # y comprobar si f (la distancia a la meta) es la menor
            if(neighbor not in clear):
                # Si es valido, entonces agregar nodo vecino a la lista abierta
                clear.append(neighbor)
    
    # Retornar none si no se encuentra ningun camino
    return None

# The main entry point for this module
def main():
    
    ###################################################################################################
    generator = map_gen()

    #mapa nxm
    #n filas
    #m columnas
    n=8
    m=16
    
    
    arr =generator.generate_map(n,m)
    
    
    # generar posicion de inicio
    # START 
    start_i = randrange(n-1) #fila de inicio
    start_j = randrange(m-1) #columna de inicio
    
    # generar posicion de termino
    # GOAL
    goal_i = randrange(n-1)
    goal_j = randrange(m-1)

    # Probar que la posicion de inicio y fin no sean la misma
    while(start_i == goal_i and start_j == goal_j):
        start_i = randrange(n-1)
        start_j = randrange(m-1)

        goal_i = randrange(n-1)
        goal_j = randrange(m-1)

    arr[start_i][start_j] = 3
    arr[goal_i][goal_j] = -1
    
    
    """
    # generar posicion de inicio FIJA
    # START 
    start_i = 1 #fila de inicio
    start_j = 1 #columna de inicio
    
    # generar posicion de termino FIJA
    # GOAL
    goal_i = (n-1)
    goal_j = (m-1)
    """
    ###################################################################################################
    
    
    # Get a map (grid)
    start = (start_i, start_j)
    end = (goal_i, goal_j)
    # clear a file
    
    #Generar orientacion inicial del robot)
    o = ["N", "S", "E", "O"]
    random.shuffle(o)

    # generar el SPIRIT
    sprt = SPIRIT(start_i, start_j, o.pop())
      
    print("Start: {0} ,Goal: {1} ".format((start_i, start_j), (goal_i, goal_j)))
    print("Initial Orientation: ", sprt.orientation)

    # comenzar a contar tiempo
    start_time = datetime.datetime.now()
    
    best_first_search(arr, start, end, sprt)
    
    # terminar de contar tiempo
    end_time = datetime.datetime.now()
    
    #Calcular milisegundos
    time_diff = (end_time - start_time)
    execution_time = time_diff.total_seconds() * 1000
    
    
    remap = np.array(arr, dtype='O')
    remap[remap==0]='-'
    remap[remap==1]='#'
    remap[remap==2]='X'
    remap[remap==-1]='O'
    remap[remap==3]='S'

    path_map = np.array(remap)

    for tile in sprt.path:
        path_map[tile]="+"
    print(remap)
    print('\n=====================================================================================================\n')
    print(path_map)
    print('Path: ',sprt.path)
    print("Turns: ", sprt.turns)
    print("Time: ", sprt.time)
    print("Tiempo de ejecucion del algoritmo: ",execution_time, " milisegundos")
    print("Tamaño del mapa: ",n*m, " [m2]")

# Tell python to run main method
if __name__ == "__main__": main()