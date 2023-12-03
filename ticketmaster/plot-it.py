#
# import numpy as np
# import matplotlib.pyplot as plt

def plot-it():
    x = np.random.randn(1000)
    plt.hist(x, bins=20)
    plt.show()

    plt.hist(x, bins=range(-4, 5))
    plt.show()

    plt.hist(x, bins=20, histtype='step', linewidth=2)
    plt.show()

    plt.hist(x, bins=20, rwidth=0.8)
    plt.show()

    plt.hist(x, bins=20, rwidth=0.8, edgecolor='darkgreen')
    plt.show()

    plt.hist(x, bins=20, rwidth=0.8, edgecolor='red')
    plt.show()

    plt.hist(x, bins=20, rwidth=0.7, edgecolor='red')

    plt.savefig('plot.png')
### plt.show()

# // In jQuery
# $("#imageContainer").html('<img src="plot.png">');
