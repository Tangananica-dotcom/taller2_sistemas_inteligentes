import numpy as np
from SPIRIT import SPIRIT
from map_gen import map_gen
import sys
np.set_printoptions(threshold=sys.maxsize)
from scipy.ndimage.interpolation import zoom

generator = map_gen()
arr =generator.generate_map(6,12)


arr = np.array_str(arr, max_line_width=500)
print(arr)

sprt = SPIRIT()
print(sprt.pos, sprt.time, sprt.orientation)
sprt.rotate_left()
print(sprt.pos, sprt.time, sprt.orientation)
sprt.rotate_right()
print(sprt.pos, sprt.time, sprt.orientation)
sprt.commit()

print(sprt.pos, sprt.time, sprt.orientation)