import numpy as np

from manim_express_tests.tests_import import *

scene = EagerModeScene()

theta  = np.linspace(0, TAU, 10000)
x = np.cos(theta)
y = np.sin(theta)
# x += random_trigonometric(x, intensity=0.003)
# y += dy
# scene.plot(x, y, axes_ratio=1)
# scene.plot(theta, dy)
# scene.plot(theta, y)
scene.plot(x, rand_func(y, intensity=0.2), axes_ratio=1)
# scene.plot(x, y, axes_ratio=1)
# scene.plot(x, dy)

scene.show_plot()

scene.hold_on()