import numpy as np
import operator

class SPIRIT():
    left_switcher ={
        "E":"N",
        "N":"O",
        "O":"S",
        "S":"E"
    }
    right_switcher = {
        "E": "S",
        "S": "O",
        "O": "N",
        "N": "E"
    }
    double_switcher = {
        "E": "O",
        "N": "S",
        "O": "E",
        "S": "N"
    }
    commit_switcher={
        "E":(0, 1),
        "O":(0, -1),
        "N":(-1, 0),
        "S":(1, 0)
    }
    weights = {
        "rotar":4,
        "rotar2":8,
        -1:0,
        1:2,
        0:5/6
    }
    def __init__(self, x = 0, y = 0, o = "E"):
        self.pos=(x, y)
        self.orientation = o
        self.time = 0.0
        self.path = [self.pos]
        self.turns = []
    def weight_turn(self, o = 'E'):
        c = 0
        if(self.double_switcher.get(self.orientation)==o):
            c = self.weights.get("rotar2")
        elif self.orientation!=o:
            c = self.weights.get("rotar")
        return c
    def rotate_left(self):
        self.orientation = self.left_switcher.get(self.orientation)
        self.time += self.weights.get("rotar")
        self.turns.append([self.pos, self.orientation])
    def rotate_right(self):
        self.orientation = self.right_switcher.get(self.orientation)
        self.time += self.weights.get("rotar")
        self.turns.append([self.pos, self.orientation])
    def double_rotation(self):
        self.orientation = self.double_switcher.get(self.orientation)
        self.time += self.weights.get("rotar2")
        self.turns.append([self.pos, self.orientation])
    def commit(self, type=0, o="E", next=(0,0)):
        if(self.orientation != o):
            if self.left_switcher.get(self.orientation)==o:
                self.rotate_left()
            elif self.right_switcher.get(self.orientation)==o:
                self.rotate_right()
            else:
                self.double_rotation()
        # self.pos=tuple(map(operator.add, self.pos,self.commit_switcher.get(self.orientation)))
        self.pos=next
        self.path.append(self.pos)
        self.time+=self.weights.get(type)
        
