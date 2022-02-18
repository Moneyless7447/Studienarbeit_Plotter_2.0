import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from matplotlib.widgets import Button
import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class Plotter:
    def __init__(self, robot):
        self.robot = robot
        #plt.ion()
        self.fig = plt.figure()

        #plt.ion()

        self.axes = self.fig.add_subplot(111, projection='3d')

        self.plot(self.robot.root, self.axes, root=True)

        self.axes.set(xlim3d=(-7, 7), xlabel='x')
        self.axes.set(ylim3d=(-7, 7), ylabel='y')
        self.axes.set(zlim3d=(-7, 7), zlabel='z')
        self.axes.grid(False)


        self.axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.bnext = Button(self.axnext, 'Next')
        self.bnext.on_clicked(self.set_joint_and_update)


        plt.ion()
        plt.show()
        plt.draw()
        #plt.pause(3)
        #bnext.on_clicked(self.update)

    def plot(self, joint, axes, matrix=np.identity(4), root=False):
        scale = 1 if not root else 2.1
        # Punkte für Ursprung und Koordinatenachsen für Koordinatenursprünge
        origin_point = np.dot(matrix, [0, 0, 0, 1])[:3]
        x_axis_point = np.dot(matrix, [scale, 0, 0, 1])[:3]
        y_axis_point = np.dot(matrix, [0, scale, 0, 1])[:3]
        z_axis_point = np.dot(matrix, [0, 0, scale, 1])[:3]

        # Ursprünge als Punkte
        axes.plot([origin_point[0]], [origin_point[1]], [origin_point[2]], 'k.')
        # Achsen als Geraden
        axes.plot([origin_point[0], x_axis_point[0]], [origin_point[1], x_axis_point[1]],
                  [origin_point[2], x_axis_point[2]], 'r-', linewidth=0.5*scale)
        axes.plot([origin_point[0], y_axis_point[0]], [origin_point[1], y_axis_point[1]],
                  [origin_point[2], y_axis_point[2]], 'g-', linewidth=0.5*scale)
        axes.plot([origin_point[0], z_axis_point[0]], [origin_point[1], z_axis_point[1]],
                  [origin_point[2], z_axis_point[2]], 'b-', linewidth=0.5*scale)
        # Namen bzw. Titel anzeigen
        #axes.text(origin_point[0], origin_point[1], origin_point[2], joint.title)
        axes.text(origin_point[0], origin_point[1], origin_point[2], joint.name, fontsize = 'small')

        # # 3D Körper (Zylinder, Würfel) für verschiedene Gelenktypen
        # scale_cylinder = 0.3
        # # return evenly spaced numbers of a specified interval
        # u = np.linspace(0, 2 * np.pi, num=10)
        # v = np.linspace(0, np.pi, num=10)
        #
        # # compute the outer product (Dyadisches Produkt) of two vectors
        # x = 10 * np.outer(np.cos(u), np.sin(v))
        # y = 10 * np.outer(np.sin(u), np.sin(v))
        # z = 10 * np.outer(np.zeros(np.size(u)), np.cos(v))
        # axes.plot_surface(x, y, z, color='b')

        # Make data
        # u = np.linspace(0, 2 * np.pi, 10)
        # v = np.linspace(0, np.pi, 10)
        # x = 10 * np.outer(np.cos(u), np.sin(v))
        # y = 10 * np.outer(np.sin(u), np.sin(v))
        # z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))

        # Plot the surface
        # axes.plot_surface(x, y, z, color='b')

        #self.plot_plane()
        self.plot_cylinder(origin_point, matrix)

        if joint.children is None:
            return

        # Verbindungslinien zwischen Koordinatenursprüngen
        for index, child in enumerate(joint.children):
            child_matrix = np.dot(matrix, joint.transformationmatrices_to_children[index])
            child_point = np.dot(child_matrix, [0, 0, 0, 1])[:3]
            axes.plot([origin_point[0], child_point[0]], [origin_point[1], child_point[1]], [origin_point[2], child_point[2]],
                      'k:', linewidth=0.6)
            if not joint.has_reference_child(child.title):
                self.plot(child, axes, child_matrix)



    def update(self, argument1):
        self.axes.clear()
        self.plot(self.robot.root, self.axes, root=True)
        self.axes.grid(False)
        self.axes.set(xlim3d=(-10, 10), xlabel='x')
        self.axes.set(ylim3d=(-10, 10), ylabel='y')
        self.axes.set(zlim3d=(-10, 10), zlabel='z')
             #plt.show()
        # self.fig.show()
        plt.draw()
        #plt.pause(2)
        plt.show(block=False)
        #plt.show()



    def plotter_show(self):

        plt.show(block=True)

    def wait(self, time_in_sec):
        time.sleep(time_in_sec)

    def print_button_clicked(self, _):
        print("button_clicked")


    def set_joint_and_update(self, _):
        # self.robot.set_joint("Alpha1-Gelenk", math.radians(20))
        # self.robot.set_joint("Beta1-Gelenk", math.radians(-20))
        # self.robot.set_joint("Beta2-Gelenk", math.radians(-20))
        self.robot.set_joint("Gamma1-Gelenk", math.radians(90), math.radians(90))
        # self.robot.set_joint("Beta1-Gelenk", math.radians(-20))
        self.update(None)

    def plot_plane(self):
        # x = [1, 0, 3, 4]
        # y = [0, 5, 5, 1]
        # z = [1, 3, 4, 0]
        # x_2 = [8, 7, 5, 5]
        # y_2 = [3, 3, 2, 5]
        # z_2 = [2, 1.3, 2, 0]
        # x_3 = [0, 0, 5, 5]
        # y_3 = [-2, 0, 0, -2]
        # #y_3 = [0, 0, 0, 0]
        # z_3 = [0, 4, 0, 4]
        # x_3 = [0, 4, 0]
        # y_3 = [0, 0, 0]
        # z_3 = [0, 4, 4]


        #vertices = [list(zip(x, y, z))]
        #vertices_2 = [list(zip(x_2, y_2, z_2))]
        #vertices_3 = [list(zip(x_3, y_3, z_3))]
        #print(vertices)
        #poly = Poly3DCollection(vertices, alpha=0.5)
        #self.axes.add_collection3d(poly)
        #poly_2 = Poly3DCollection(vertices_2, alpha=0.5)
        #self.axes.add_collection3d(poly_2)
        #poly_3 = Poly3DCollection(vertices_3, alpha=0.5)
        #self.axes.add_collection3d(poly_3)

    def plot_cylinder(self, start_point, trans_matrix):
        r = 0.3
        h = 0.5

        # # 1_1. Teilseitenflaeche
        x_1_1 = [0, 0, (math.sqrt(2) / 2) * r]
        y_1_1 = [r, r, (math.sqrt(2) / 2) * r]
        z_1_1 = [-h, h, -h]

        ############
        ############
        ###########
        # Das als externe funktion ########
        vertices_1_1 = [np.dot(trans_matrix, [x_1_1[0], y_1_1[0], z_1_1[0], 1]),
                        np.dot(trans_matrix, [x_1_1[1], y_1_1[1], z_1_1[1], 1]),
                        np.dot(trans_matrix, [x_1_1[2], y_1_1[2], z_1_1[2], 1])]


        vertices_1_1_2 = [[[]] for i in range(3)]
        for point in range(3):
            vertices_1_1_2[point][0].append(vertices_1_1[point][0])
            vertices_1_1_2[point][0].append(vertices_1_1[point][1])
            vertices_1_1_2[point][0].append(vertices_1_1[point][2])
            vertices_1_1[point] = tuple(vertices_1_1_2[point][0])

        vertices_1_1 = [vertices_1_1]

        poly_1_1 = Poly3DCollection(vertices_1_1, alpha=0.5)
        self.axes.add_collection3d(poly_1_1)

        #1_2 Teilseitenfläche
        x_1_2 = [0, (math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r]
        y_1_2 = [r, (math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r]
        z_1_2 = [h, -h, h]

        vertices_1_2 = [np.dot(trans_matrix, [x_1_2[0], y_1_2[0], z_1_2[0], 1]),
                        np.dot(trans_matrix, [x_1_2[1], y_1_2[1], z_1_2[1], 1]),
                        np.dot(trans_matrix, [x_1_2[2], y_1_2[2], z_1_2[2], 1])]
        # print(f"vertices_1_2 {vertices_1_2}")

        vertices_1_2_2 = [[[]] for i in range(3)]
        for point in range(3):
            vertices_1_2_2[point][0].append(vertices_1_2[point][0])
            vertices_1_2_2[point][0].append(vertices_1_2[point][1])
            vertices_1_2_2[point][0].append(vertices_1_2[point][2])
            vertices_1_2[point] = tuple(vertices_1_2_2[point][0])

        vertices_1_2 = [vertices_1_2]

        poly_1_2 = Poly3DCollection(vertices_1_2, alpha=0.5)
        self.axes.add_collection3d(poly_1_2)