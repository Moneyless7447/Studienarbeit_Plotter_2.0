import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib.widgets import Button


class Plotter:
    def __init__(self, robot):
        self.robot = robot
        #plt.ion()
        self.fig = plt.figure() ###
        #plt.ion()
        self.axes = self.fig.add_subplot(111, projection='3d')

        self.plot(self.robot.root, self.axes, root=True)

        self.axes.set(xlim3d=(-7, 7), xlabel='x')
        self.axes.set(ylim3d=(-7, 7), ylabel='y')
        self.axes.set(zlim3d=(-7, 7), zlabel='z')



        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(self.update)
        #bnext.on_clicked(print("button clicked"))
        ###plt.show()

        plt.ion()
        plt.show()
        plt.draw()
        plt.pause(3)
        #bnext.on_clicked(self.update)

    def plot(self, joint, axes, matrix=np.identity(4), root=False):

        scale = 1 if not root else 2.1
        origin_point = np.dot(matrix, [0, 0, 0, 1])[:3]
        x_axis_point = np.dot(matrix, [scale, 0, 0, 1])[:3]
        y_axis_point = np.dot(matrix, [0, scale, 0, 1])[:3]
        z_axis_point = np.dot(matrix, [0, 0, scale, 1])[:3]

        axes.plot([origin_point[0]], [origin_point[1]], [origin_point[2]], 'k.')
        axes.plot([origin_point[0], x_axis_point[0]], [origin_point[1], x_axis_point[1]],
                  [origin_point[2], x_axis_point[2]], 'r-', linewidth=0.5*scale)
        axes.plot([origin_point[0], y_axis_point[0]], [origin_point[1], y_axis_point[1]],
                  [origin_point[2], y_axis_point[2]], 'g-', linewidth=0.5*scale)
        axes.plot([origin_point[0], z_axis_point[0]], [origin_point[1], z_axis_point[1]],
                  [origin_point[2], z_axis_point[2]], 'b-', linewidth=0.5*scale)
        #axes.text(origin_point[0], origin_point[1], origin_point[2], joint.title)

        if joint.children is None:
            return
        for index, child in enumerate(joint.children):
            child_matrix = np.dot(matrix, joint.transformationmatrices_to_children[index])
            child_point = np.dot(child_matrix, [0, 0, 0, 1])[:3]
            axes.plot([origin_point[0], child_point[0]], [origin_point[1], child_point[1]], [origin_point[2], child_point[2]],
                      'k:', linewidth=0.4)

            self.plot(child, axes, child_matrix)



    def update(self, argument1):
        self.axes.clear()
        self.plot(self.robot.root, self.axes, root=True)
        self.axes.set(xlim3d=(-7, 7), xlabel='x')
        self.axes.set(ylim3d=(-7, 7), ylabel='y')
        self.axes.set(zlim3d=(-7, 7), zlabel='z')
             #plt.show()
        # self.fig.show()
        plt.draw()
        plt.pause(2)
        plt.show(block=False)



    def plotter_show(self):

        plt.show(block=True)

    def wait(self, time_in_sec):
        time.sleep(time_in_sec)

