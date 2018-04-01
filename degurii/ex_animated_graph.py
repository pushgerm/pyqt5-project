import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
ax.set_xlim((0, 3000))
ax.set_ylim((156, 170))
ax.grid(True)

line, = ax.plot([], [], lw = 2)

input = np.loadtxt('temp.csv', delimiter=',', dtype=np.float32)  # 파일의 절대경로를 넣어준다
ndata = input.shape[0]



def init():
    line.set_data(([], []))
    return (line, )

def animate(t):
    x = [i for i in range(0, t)]
    y = input[:t, 4:5]
    line.set_data(x, y)

    return line,

ani = animation.FuncAnimation(fig=fig, func=animate, init_func=init, interval=20, blit=True)

plt.show()