import imp


import numpy as np

def euclidean_distance(color1, color2):
    return np.linalg.norm(np.array(color1) - np.array(color2))