import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import time
# random_matrix = np.random.rand(100, 100) * 10
# fig = plt.figure('matrix configuration')
# ax = fig.add_subplot(111)
# heatmap = ax.pcolor(random_matrix, cmap = plt.cm.Reds)
# heatmap = ax.pcolor(random_matrix)
# heatmap = ax.pcolor(random_matrix, cmap=cm.coolwarm)

# cax = ax.imshow(random_matrix, interpolation='nearest', cmap=cm.cool)
# ax.set_frame_on(False)
# cax = ax.imshow(random_matrix, cmap=cm.coolwarm)
# cbar = fig.colorbar(cax, ticks=[-1, 0, 10])
# plt.show()

# currentTime = time.time()
# counter = 200
# while counter > 0:
#     random_matrix = np.random.rand(100, 100) * 10
#     time.sleep(0.05)
#     cax = ax.imshow(random_matrix, cmap=cm.coolwarm)
#     cbar = fig.colorbar(cax, ticks=[-1, 0, 10])
#     counter -= 1
#     plt.draw()

# plt.axis([0, 1000, 0, 1])
fig = plt.figure('matrix configuration')
ax = fig.add_subplot(111)
plt.ion()
plt.show()

random_matrix = np.random.rand(100, 100) * 10
cax = ax.imshow(random_matrix, cmap=cm.coolwarm)
cbar = fig.colorbar(cax, ticks=[-1, 0, 10])
for i in range(1000):
    random_matrix = np.random.rand(100, 100) * 10
    cax = ax.imshow(random_matrix, cmap=cm.coolwarm)
    # cbar = fig.colorbar(cax, ticks=[-1, 0, 10])
    plt.draw()
    time.sleep(0.1)