import numpy as np
from scipy import stats

def normal(mean, std, color="black", num_points=200):
    x = np.linspace(mean-6*std, mean+6*std, num_points)
    