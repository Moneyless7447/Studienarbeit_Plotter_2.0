import matplotlib.pyplot as plt
import numpy as np
import math
from robot import *
from joint import *
from plotter import *
import json
from mpl_toolkits.mplot3d import Axes3D
import os
import time


if __name__ == '__main__':
    print('Start robot: \n')
    robot = Robot("test_roboter", "example_robot_dh.json")
    print(f"robot: {robot.root}")
    print(f"dh to A: {robot.generate_dh_matrix_from_to('root', 'Beta1-Gelenk')}")
    robot.set_joint("Alpha1-Gelenk", math.radians(180))
    print(f"dh to A: {robot.generate_dh_matrix_from_to('root', 'Beta1-Gelenk')}")
    plotter = Plotter(robot)
    plotter.update()
    counter = 0
    direction = 1
    while True:
        time.sleep(3)
        robot.set_joint("Alpha1-Gelenk", math.radians(90)*counter)
        print(f"dh to A: {robot.generate_dh_matrix_from_to('root', 'Beta1-Gelenk')}")
        plotter.update()
        counter = counter+(0.1*direction)
        if counter >= 1:
            direction = -1
        elif counter <= 0:
            direction = 1
        print(counter)