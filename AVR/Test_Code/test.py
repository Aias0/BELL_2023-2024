import numpy as np
arr = [[0 for _ in range(8)] for _ in range(8)]
arr[2][2] = 1

print(np.all(np.array(arr) == 0))