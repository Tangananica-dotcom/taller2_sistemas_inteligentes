class Node():

    def __init__(self, position:(), parent:(), value =0, o='X'):
        self.position = position # Posicion del nodo
        self.parent = parent # nodo padre
        self.orientation = o
        self.type = value
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