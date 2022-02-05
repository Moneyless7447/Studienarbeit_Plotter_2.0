import matplotlib.pyplot as plt
import numpy as np
import math
from robot import *
from joint import *
import json
from mpl_toolkits.mplot3d import Axes3D
import os

if __name__ == '__main__':
    robot = Robot("test_roboter")
    treestructure = robot.restructure_json("example_robot_dh.json")
    print('Start robot: \n')
    print(f"treestructure: {treestructure}")
