import numpy as np
import matplotlib.pyplot as plt



class Plotter:
    def __init__(self, robot):
        self.robot = robot
        self.fig = plt.figure()
        #plt.ion()
        self.axes = self.fig.add_subplot(111, projection='3d')
        # self.plot(self.robot.root, self.axes, root=True)
        self.axes.set_xlim3d([-7, 7])
        self.axes.set_ylim3d([-7, 7])
        self.axes.set_zlim3d([-7, 7])
        #plt.show()
        # plt.plot()

    def plot(self, joint, axes, matrix=np.identity(4), root=False):
        axes.clear()

        scale = 1 if not root else 2.1
        origin_point = np.dot(matrix, [0, 0, 0, 1])[:3]
        x_axis_point = np.dot(matrix, [scale, 0, 0, 1])[:3]
        y_axis_point = np.dot(matrix, [0, scale, 0, 1])[:3]
        z_axis_point = np.dot(matrix, [0, 0, scale, 1])[:3]

        axes.plot([origin_point[0]], [origin_point[1]], [origin_point[2]], 'k.')
        axes.plot([origin_point[0],x_axis_point[0]], [origin_point[1], x_axis_point[1]],
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

        self.fig.show()

    def update(self):
        self.plot(self.robot.root, self.axes, root=True)