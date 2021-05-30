import numpy as np
from SPIRIT import SPIRIT
from map_gen import map_gen
import sys
np.set_printoptions(threshold=sys.maxsize)
from scipy.ndimage.interpolation import zoom
from random import randrange
    
    
# Esta clase representa un nodo
class Node:
    # Inicializar la clase
    def __init__(self, position:(), parent:()):
        self.position = position # Posicion del nodo
        self.parent = parent # nodo padre
        self.h = 0 # Distancia al nodo objetivo (goal)
    
    # Comparar nodos
    def __eq__(self, other):
        return self.position == other.position
    
    # Sort a los nodos
    def __lt__(self, other):
         return self.h < other.h
    
    # Print a los nodos
    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.h))

# Dibujar el mapa por consola
def draw_grid(map, width, height, spacing=2, **kwargs):
    for y in range(height):
        for x in range(width):
            print('%%-%ds' % spacing % draw_tile(map, (x, y), kwargs), end='')
        print()

# Dibujar un cuadrante
def draw_tile(map, position, kwargs):
    
    # Get the map value
    value = map.get(position)
    # Check if we should print the path
    if 'path' in kwargs and position in kwargs['path']: value = '+'
    # Check if we should print start point
    if 'start' in kwargs and position == kwargs['start']: value = '@'
    # Check if we should print the goal point
    if 'goal' in kwargs and position == kwargs['goal']: value = '$'
    # Return a tile value
    return value 

# Algoritmo Best-first
def best_first_search(map, start, end):
    
    # Cree listas para nodos abiertos y nodos cerrados
    open = [] #lista open
    closed = [] #lista closed
    
    # Crea un nodo de inicio y un nodo objetivo
    start_node = Node(start, None)
    goal_node = Node(end, None)
    
    # Para comenzar, agregamos el nodo de inicio a la lista open
    open.append(start_node)
    
    # Loop hasta que la lista abierta (lista open) esté vacía
    while len(open) > 0:
        
        # Sort a la lista abierta para obtener primero el nodo con el costo más bajo
        open.sort()
        
        # Obtener el nodo con el menor costo
        current_node = open.pop(0)
        
        # Agregar el nodo actual a la lista cerrada (lista closed)
        closed.append(current_node)
        
        # Comprobar si se a llegado a la meta, retorna el camino (retorna path)
        if current_node == goal_node:
            path = []
            while current_node != start_node:
                path.append(current_node.position)
                current_node = current_node.parent
            path.append(start) 
            # Retorna el camino inverso
            return path[::-1]
        
        # Obtener la posición actual del nodo
        (x, y) = current_node.position
        
        # Obtener los vecinos del nodo
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        
        # Loop a los vecinos del nodo
        for next in neighbors:
            
            # Obtener el tipo de terreno (value)
            map_value = map.get(next)
            
            # Con el value, comprobar si el nodo es una pared (obstaculo).
            if(map_value == '#'):
                continue
            
            # Si no es una pared, entonces es valido y creamos un nodo vecino
            neighbor = Node(next, current_node)
            
            # Comprobar si el nodo vecino está en la lista cerrada
            if(neighbor in closed):
                continue
            
            # Si no esta en la lista cerrada, entonces es un nodo valido, y generamos la heurística
            # (distancia al nodo destino) (distancia Manhattan)
            neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1])
            
            # Comprobar si el nodo vecino está en la lista abierta
            # y comprobar si f (la distancia a la meta) es la menor
            if(add_to_open(open, neighbor) == True):
                # Si es valido, entonces agregar nodo vecino a la lista abierta
                open.append(neighbor)
    
    # Retornar none si no se encuentra ningun camino
    return None

# Comprobar si se debe agregar un nodo vecino a la lista abierta
def add_to_open(open, neighbor):
    for node in open:
        if (neighbor == node):
            return False
    return True

# Funcion para calcular la cantidad de giros que tiene que hacer el spirit al recorrer el camino
def calcular_cantidad_giros(path, orientacion_inicial):
    
    #orientacion actual
    oa = orientacion_inicial
    
    #orientacion del paso siguiente que tiene que dar el spirit
    o_s = "X"
    
    
    #longitud de la lista path
    longitud = len(path)
    
    #cantidad de giros que tiene que dar el spirit
    cantidad_giros = 0
    
    for i in range(longitud):
        
        a = i #numero cuadrante actual
        b = i+1 #numero siguiente cuadrante
        
        if(b==longitud):
            break
        
        #cuadrante actual en donde se encuentra el spirit
        cuadrante_inicial = path[a]
        
        #siguiente cuadrante en el camino que tiene que tomar el spirit
        next_cuadrante = path[b]
        
        #coordenadas x,y
        # x las columnas
        # y las filas
        print("Posicion actual: ", path[a], ", Orientacion actual: ", oa)

        #hay que girar?
        if(next_cuadrante[0] > cuadrante_inicial[0]):
            #derecha
            #se mueve al Este
            o_s = "E"
            
        elif(next_cuadrante[0] < cuadrante_inicial[0]):    
            #se mueve al Oeste
            #izquierda
            o_s = "O"
            
        if(next_cuadrante[1] > cuadrante_inicial[1]):
            #abajo
            #se mueve al Sur
            o_s = "S"
        
        elif(next_cuadrante[1] < cuadrante_inicial[1]):    
            #se mueve al Norte
            o_s = "N"
        
        # Si tiene que girar de norte a sur el spirit tiene que girar 2 veces
        if(oa == "N" and o_s == "S"):
            cantidad_giros += 2 #2 giros
            oa = o_s            #orientacion siguiente pasa a ser la orientacion actual
        
        # Si tiene que girar de norte a este, o de norte a oeste, el spirit tiene que girar 1 vez
        elif((oa == "N" and o_s == "E") or (oa == "N" and o_s == "O")):
            cantidad_giros += 1
            oa = o_s

        # Si tiene que girar de sur a norte el spirit tiene que girar 2 veces
        if(oa == "S" and o_s == "N"):
            cantidad_giros += 2
            oa = o_s
        
        # Si tiene que girar de sur a este, o de sur a oeste, el spirit tiene que girar 1 vez
        elif((oa == "S" and o_s == "E") or (oa == "S" and o_s == "O")):
            cantidad_giros += 1
            oa = o_s


        if(oa == "E" and o_s == "O"):
            cantidad_giros += 2
            oa = o_s
        elif((oa == "E" and o_s == "S") or (oa == "E" and o_s == "N")):
            cantidad_giros += 1
            oa = o_s
        

        if(oa == "O" and o_s == "E"):
            cantidad_giros += 2
            oa = o_s
        elif((oa == "O" and o_s == "S") or (oa == "O" and o_s == "N")):
            cantidad_giros += 1
            oa = o_s
        
        print("next cuadrante: ", next_cuadrante, ", next orientacion: ", o_s)
        print("=====")
        
    print("cantidad de giros: ", cantidad_giros)

    return cantidad_giros

def calcular_tiempo(map, path):
    tiempo_terreno = 0
    

    #longitud de la lista path
    longitud = len(path)
    
    
    for i in range(longitud):
        
        a = i #numero cuadrante actual
        
        if(a==longitud-1):
            break
        
        #cuadrante actual en donde se encuentra el spirit
        cuadrante_actual = path[a]
        
        # Get the map value
        value = map.get(cuadrante_actual)
        #print("el cuadrante: ", cuadrante_actual, "tiene el valor: ", value)
        if(value == "_"):
            tiempo_terreno += 5/6
        elif(value == "."):
            tiempo_terreno += 2
    
    #print("tiempo terreno: ", tiempo_terreno)
    
    return tiempo_terreno 


# The main entry point for this module
def main():
    
    sprt = SPIRIT()
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
    
    posicion_correcta = False
    
    while(posicion_correcta != True):
        
        
        if(start_i == goal_i and start_j == goal_j):
            posicion_correcta = False
            
            start_i = randrange(n-1)
            start_j = randrange(m-1)
            
            # generar posicion de termino
            # GOAL
            goal_i = randrange(n-1)
            goal_j = randrange(m-1)
        else:
            posicion_correcta = True
                
    
    
    #arr = np.array_str(arr, max_line_width=500)
    print(arr)
    
    
    #mapa.txt es el mapa generado por nosotros
    #cambiar a maze2.txt para probar con un mapa de prueba
    f= open("mapa.txt","w+")
    
    
    # Generar la primera y ultima linea, las cuales "cierran" el mapa
    top_line = "#"
    
    for i in range(m):
        top_line += "#"
    
    top_line += "#"
    # "cerrar" el mapa por la parte superior
    f.write(top_line + "\n")
    
    #la cantidad de lineas del archivo txt es igual a m
    for i in range(n):
        #print("La fila: ", i)
        # comenzar una fila con "#", para "cerrar" el mapa por la parte izquierda
        line = "#"
        array = arr[i]
        le = len(arr[i])
        for j in range(le):
            
            #caracter que va cambiando
            c = ""
            #print("La columna: ", j)
            if(start_i == i and start_j == j):
                c = "@"
            elif(goal_i == i and goal_j == j):
                c = "$"
            elif array[j] == 0:
                c = "_"
            elif array[j] == 1:
                c = "."
            elif array[j] == 2:
                c = "#"
            line += c
        
        #terminar la fila con "#", para "cerrar" el mapa por la parte derecha
        line += "#"
        f.write(line + "\n")
         
    # "cerrar" el mapa por la parte de abajo
    f.write(top_line)
    
    # terminar de generar el archivo
    f.close() 
    
    
    print(start_i, start_j)
    
    print(goal_i, goal_j)
    ###################################################################################################
    
    
    # Get a map (grid)
    map = {}
    chars = ['c']
    start = None
    end = None
    width = 0
    height = 0
    # Open a file
    fp = open('mapa.txt', 'r')
    
    #Generar orientacion inicial del robot
    orientacion_inicial = "X"
    orientRand = randrange(3)
    if(orientRand == 0):
        orientacion_inicial = "N"  
    elif(orientRand == 1):
        orientacion_inicial = "S"
    elif(orientRand == 2):
        orientacion_inicial = "E"
    elif(orientRand == 3):
        orientacion_inicial = "O"

    tiempo_terreno = 0
    
    
    
    # Loop until there is no more lines
    while len(chars) > 0:
        # Get chars in a line
        chars = [str(i) for i in fp.readline().strip()]
        # Calculate the width
        width = len(chars) if width == 0 else width
        # Add chars to map
        for x in range(len(chars)):
            map[(x, height)] = chars[x]
            if(chars[x] == '@'):
                start = (x, height)
            elif(chars[x] == '$'):
                end = (x, height)
        
        # Increase the height of the map
        if(len(chars) > 0):
            height += 1
    # Close the file pointer
    fp.close()
    # Find the closest path from start(@) to end($)
    path = best_first_search(map, start, end)

    print("Camino recorrido:")
    print(path)
    
    
    print("==========================================================================")
    print("Giros del robot: ")
    cantidad_giros = calcular_cantidad_giros(path, orientacion_inicial)
    
    print("==========================================================================")
    print()
    
    #los signos "+" es el camino recorrido
    print("Mapa:")
    draw_grid(map, width, height, spacing=1, path=path, start=start, goal=end)
    print()
    print('Numero de cuadrantes recorridos para llegar a la meta: {0}'.format(len(path)))
    
    tiempo_terreno = calcular_tiempo(map, path)
    
    print()
    print("El SPIRIT se demora: ", tiempo_terreno + 4*cantidad_giros, " segundos en recorrer el camino.")
    
    sprt.commit()
    
    #print("El SPIRIT se demora: ")
    #print(sprt.pos, sprt.time, sprt.orientation)
# Tell python to run main method
if __name__ == "__main__": main()