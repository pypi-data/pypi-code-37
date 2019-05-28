import matplotlib
import matplotlib.pylab as plt

from SecretColors.palette import Palette, ColorMap

p = Palette()
c = ColorMap(matplotlib, p)

x = p.random(shade=40, no_of_colors=3)

for i, v in enumerate(x):
    plt.bar(i, 1, color=v)

plt.show()
