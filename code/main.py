import matplotlib.pyplot as plt
import numpy as np
import math
from robot import *
from joint import *
import json
from mpl_toolkits.mplot3d import Axes3D
import os

if __name__ == '__main__':
    print('Start robot: \n')
    robot = Robot("test_roboter")
    #treestructure = robot.restructure_json("example_robot_dh.json")

    #print(f"treestructure: {treestructure}")
    #print(f"rootelements von robot: {getattr(robot, 'rootelements')}")
    print(f"kin_chain_list test: {robot.init_kin_chain('1')}")
    print(f"treestructure von robot: {getattr(robot, 'treestructure')}")
    #print(f"test twist {treestructure['1.1.1'].offset}")
