import numpy as np

# def create_map(m, n):
#     return np.random.randint(low=0, high=1, size=(1,4))

# print(create_map(3, 2))

import sys
np.set_printoptions(threshold=sys.maxsize)
from scipy.ndimage.interpolation import zoom
arr = np.random.uniform(size=(4,4))
arr = zoom(arr, 8)
arr = arr > 0.5
arr = np.where(arr, '-', '#')
arr = np.array_str(arr, max_line_width=500)
print(arr)