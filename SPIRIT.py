import numpy as np

class SPIRIT():
    left_switcher ={
        "este":"norte",
        "norte":"oeste",
        "oeste":"sur",
        "sur":"este"
    }
    right_switcher = {
        "este": "sur",
        "sur": "oeste",
        "oeste": "norte",
        "norte": "este"
    }
    commit_switcher={
        "este":[1, 0],
        "oeste":[-1, 0],
        "norte":[0, -1],
        "sur":[0, 1]
    }
    weights = {
        "rotar":4,
        "abrupto":2,
        "llano":5/6
    }
    def __init__(self, x = 0, y = 0, o = "este"):
        self.pos=np.array([x, y])
        self.orientation = o
        self.time = 0.0
        self.movements = np.array([self.pos])
    def rotate_left(self):
        self.orientation = self.left_switcher.get(self.orientation)
        self.time += self.weights.get("rotar")
    def rotate_right(self):
        self.orientation = self.right_switcher.get(self.orientation)
        self.time += self.weights.get("rotar")
    def commit(self, type="llano"):
        self.pos+=self.commit_switcher.get(self.orientation)
        self.movements.__add__(self.pos)
        self.time+=self.weights.get(type)
        
