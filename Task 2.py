import numpy as np
import math
from scipy import constants
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from fractions import Fraction


def surface_func(x, k):
    return k * x + 5


def func_x(t_points, x_0, acc):
    return [x_0 + (acc[0] * t ** 2) / 2 for t in t_points]


def func_y(t_points, y_0, acc):
    return [y_0 - (acc[1] * t ** 2) / 2 for t in t_points]


def velocity_func(a, t):
    return[a * i for i in t]


print('Введіть множник N перед числом pi для кута -> N * pi у форматі 1/6, 0.55, 2/3 (формат модуля Fractions для '
      'рядків)')
print('(Кут відміряється від осі X за ходом годинникової стрілки)\n')
angles = [Fraction(input(f'Введіть значення для кута {i} (Менше за 1/2 pi):\n')) for i in range(1, 3)]

k = [math.tan(math.pi * (1 - angle)) for angle in angles]
x_values = np.arange(0, 100, 1)
y_0_values = [surface_func(0, k[i]) for i in range(2)]

time_values = np.arange(0, 7, 0.05)

gravity = constants.g
m = 1
friction_const = 0.5 # Металл - скло

acceleration = [gravity * (math.sin(angle * math.pi) - friction_const * math.cos(angle * math.pi)) for angle in angles]

accelerations_1 = [acceleration[0] * i for i in [math.cos(angles[0] * math.pi), math.sin(angles[0] * math.pi)]]
accelerations_2 = [acceleration[1] * i for i in [math.cos(angles[1] * math.pi), math.sin(angles[1] * math.pi)]]

coord_values_t_1 = (func_x(time_values, 0, accelerations_1), func_y(time_values, y_0_values[0], accelerations_1))
coord_values_t_2 = (func_x(time_values, 0, accelerations_2), func_y(time_values, y_0_values[1], accelerations_2))

velocity_points_1 = velocity_func(acceleration[0], time_values)
velocity_points_2 = velocity_func(acceleration[1], time_values)

fig, ax = plt.subplots(nrows=1, ncols=2)

rect_1 = plt.Rectangle((0, y_0_values[0]), 0.3, 0.5, color='red', angle=90 - angles[0] * 180)
rect_2 = plt.Rectangle((0, y_0_values[1]), 0.3, 0.5, color='cyan', angle=90 - angles[1] * 180)

ax[0].add_patch(rect_1)
ax[0].add_patch(rect_2)


def animate(i, x, y, x_1, y_1):
    rect_1.set_xy((x[i], y[i]))
    rect_2.set_xy((x_1[i], y_1[i]))

    return rect_1, rect_2,


myAnimation = animation.FuncAnimation(fig, animate, frames=len(time_values),
                                      fargs=(coord_values_t_1[0], coord_values_t_1[1],
                                             coord_values_t_2[0], coord_values_t_2[1]),
                                      interval=10, blit=True, repeat=True)


ax[0].set_xlim(0, 10)
ax[0].set_ylim(0, 10)

ax[0].set_title("Анімація руху об'єктів")
ax[1].set_title('Графіки залежності швидкостей від часу')

ax[0].set_xlabel('x')
ax[0].set_ylabel('y')

ax[1].set_xlabel('t')
ax[1].set_ylabel('V(t)')

ax[0].plot(x_values, [surface_func(x, k[0]) for x in x_values], c='red', label=f'Кут = pi * {angles[0]}')
ax[0].plot(x_values, [surface_func(x, k[1]) for x in x_values], c='green', label=f'Кут = pi * {angles[1]}')
ax[1].plot(time_values, velocity_points_1, c='red', label=f'Кут = pi * {angles[0]}')
ax[1].plot(time_values, velocity_points_2, c='green', label=f'Кут = pi * {angles[1]}')

ax[0].grid(True)
ax[1].grid(True)

ax[0].legend()
ax[1].legend()

plt.show()
