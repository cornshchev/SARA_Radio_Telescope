import numpy as np
import matplotlib.pyplot as plt

x= [400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600]
y = [1.8, 2.0, 2.5, 2.8, 3.2, 3.8, 4.2, 5.0, 6.0, 7.0]


fig, ax = plt.subplots()
plt.plot(x, y, marker='o')
plt.title('Frequency bias ')
plt.xlabel('Frequency (MHz)')
plt.ylabel('bias (kHz)')
plt.grid()
plt.show()