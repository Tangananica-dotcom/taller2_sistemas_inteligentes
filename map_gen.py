import numpy as np
from scipy.ndimage.interpolation import zoom


class map_gen():
    def __init__(self):
        self.z = 2

    def generate_map(self, n, m):

        if(n%self.z!=0 or m%self.z!=0):
            raise NameError("Las dimenciones deben ser multiplos de "+str(self.z))
        arr = np.random.uniform(size=(int(n/self.z), int(m/self.z)))
        arr = zoom(arr, self.z)
        arr[arr < 0.5] = 0
        arr[arr > 0.8] = 2
        arr[np.logical_and(arr >= 0.5, arr <= 0.8)] = 1
        return arr

        
