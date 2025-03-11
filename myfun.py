import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

def normal(mean, std, color="black", num_points=200):
    x = np.linspace(mean-6*std, mean+6*std, num_points)
    p = stats.norm.pdf(x, mean, std)
    plt.plot(x, p, color, linewidth=2)
