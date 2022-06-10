import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.widgets import Button
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import RadioButtons
from matplotlib.widgets import TextBox
import math
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
#from tkinter import *

class Plotter:
    def __init__(self, robot, fig=None):
        self.robot = robot
        if fig is not None:
            self.fig = fig
        else:
            self.fig = plt.figure()
        self.axes = self.fig.add_subplot(111, projection='3d')
        self.show_title = False
        self.show_name = False
        self.show_3d_symbol = False
        self.geometry_scaling_factor = 5
        self.geometry_scaling_factor_2 = 25
        self.geometry_scaling = self.get_max_dh_param(self.robot.root) * self.geometry_scaling_factor / self.geometry_scaling_factor_2
        origin_points = self.plot(self.robot.root, self.axes, root=True)
        calculated_limits = self.calc_limits(origin_points)
        self.axes.set(xlim3d=(calculated_limits[0], calculated_limits[1]), xlabel='X')
        self.axes.set(ylim3d=(calculated_limits[0], calculated_limits[1]), ylabel='Y')
        self.axes.set(zlim3d=(calculated_limits[0], calculated_limits[1]), zlabel='Z')
        self.axes.grid(False)


        # "Next" Button
        # self.axnext = plt.axes([0.23, 0.05, 0.08, 0.075])
        # self.bnext = Button(self.axnext, 'Next')
        # self.bnext.on_clicked(self.set_joint_and_update)
        # Checkboxen
        # self.axes_checkboxes = plt.axes([0.01, 0.82, 0.18, 0.16])
        # self.check_options = CheckButtons(self.axes_checkboxes, ["Titel", "Name", "3D Symbole"], [False, False, True])
        # self.check_options.on_clicked(self.set_show_options)
        # print(robot.get_joint_titles(robot.root))

        # # Radiobuttons
        # self.title_list = self.robot.get_joint_titles(self.robot.root)
        # self.axes_radiobox = plt.axes([0.01, 0.126, 0.3, 0.04*len(self.title_list)])
        # self.radio_joints = RadioButtons(self.axes_radiobox, self.title_list)
        # # "Apply" Button
        # self.axes_apply = plt.axes([0.15, 0.05, 0.08, 0.075])
        # self.b_apply = Button(self.axes_apply, 'Apply')
        # self.b_apply.on_clicked(self.apply_joint_change)
        # # Text Box
        # self.axes_textbox = plt.axes([0.01, 0.05, 0.14, 0.075])
        # self.text_value = TextBox(self.axes_textbox, '', initial="Test")
        # print(f"test Textbox: {self.text_value.get_active()}")
        # self.text_value.on_text_change(self.test_func)
        # self.text_value.on_submit(self.test_func)

        plt.ion()
        #plt.show()
        plt.draw()

    def set_geometry_scaling_factor(self, factor):
        '''
        Setzt einen Skalierungsfaktor für die 3D_Symbole zur unterscheidung von Rotations- und Translationsgelenken.
        '''
        #print(f"in set_geometry_scaling_factor: {self.geometry_scaling}")
        self.geometry_scaling_factor = factor
        self.set_geometry_scaling()
        self.update(None)

    def set_geometry_scaling(self):
        self.geometry_scaling = self.get_max_dh_param(self.robot.root) * self.geometry_scaling_factor / self.geometry_scaling_factor_2

    def get_geometry_scaling_factor(self):
        return self.geometry_scaling_factor


    def get_max_dh_param(self, joint):
        '''
        Gibt den maximalen Wert aller Längen (Length) und Offsets zurück,
        wird für den Startwert des Skalierungsfaktor genutzt.
        '''
        if not joint.children:
            return max(abs(joint.length), abs(joint.offset))
        else:
            child_max = max([self.get_max_dh_param(child) for child in joint.children])
            if child_max > abs(joint.length) or child_max > abs(joint.offset):
                return child_max
            else:
                return max(abs(joint.length), abs(joint.offset))

    def plot(self, joint, axes, matrix=np.identity(4), root=False):
        """
        Rekursives Plotten der Koordinatensysteme, Verbindungslinien, Anzeigenamen/Titel
        und Aufrufen der Funktion zum Plotten der 3D Symbolik, für aktuelles Gelenk(Joint).
        :param joint: Aktuelles Gelenk im rekursiven Aufruf.
        :param axes: Achsenobjekt in dem geplottet wird.
        :param matrix: Transformationsmatrix für dieses Gelenk(Joint).
        :param root: Boolean, zum ermitteln, ob das aktuelle Gelenk(Joint) ein Wurzelknoten ist.
        """
        # Skalierungsfaktor, Koordinatensystem des Basiskoordinatensystem(root)
        # nutzt einen größeren Skalierungsfaktor
        scale = 0.5 if not root else 1.5
        # Punkte für Ursprung und Koordinatenachsen für Koordinatenursprünge.
        # Matrixmultiplikation der Transformationsmatrix und der Punkte
        # (Ursprung und Hilfspunkte für Koordinatenachsen).
        origin_point = np.dot(matrix, [0, 0, 0, 1])[:3]
        x_axis_point = np.dot(matrix, [scale, 0, 0, 1])[:3]
        y_axis_point = np.dot(matrix, [0, scale, 0, 1])[:3]
        z_axis_point = np.dot(matrix, [0, 0, scale, 1])[:3]

        # Ursprünge als Punkte plotten
        if joint.type == "TCP" and self.show_3d_symbol:
            axes.plot([origin_point[0]], [origin_point[1]], [origin_point[2]], 'ko')
        else:
            axes.plot([origin_point[0]], [origin_point[1]], [origin_point[2]], 'k,')
        # Achsen als Geraden plotten (Verbindungslinien von Ursprungspunkten zu Hilfspunkten der Achsen)
        axes.plot([origin_point[0], x_axis_point[0]], [origin_point[1], x_axis_point[1]],
                  [origin_point[2], x_axis_point[2]], 'r-', linewidth=0.5*scale)
        axes.plot([origin_point[0], y_axis_point[0]], [origin_point[1], y_axis_point[1]],
                  [origin_point[2], y_axis_point[2]], 'g-', linewidth=0.5*scale)
        axes.plot([origin_point[0], z_axis_point[0]], [origin_point[1], z_axis_point[1]],
                  [origin_point[2], z_axis_point[2]], 'b-', linewidth=0.5*scale)
        # Namen bzw. Titel anzeigen
        if self.show_title:
            axes.text(origin_point[0], origin_point[1], origin_point[2], joint.title)
        if self.show_name:
            axes.text(origin_point[0], origin_point[1], origin_point[2], joint.name, fontsize = 'small')

        # Unterscheidung der Symbolik je nach Angabe der Gelenktypen
        if self.show_3d_symbol:
            if joint.type == "rotation":
                self.plot_cylinder(matrix)
            elif joint.type == "translation":
                self.plot_quader(matrix)


        # Abbruchkriterium für rekursiven Aufruf
        if joint.children is None:
            return

        # Verbindungslinien zwischen Koordinatenursprüngen
        origin_points = (list(origin_point),)
        for index, child in enumerate(joint.children):
            child_matrix = np.dot(matrix, joint.transformationmatrices_to_children[index])
            child_point = np.dot(child_matrix, [0, 0, 0, 1])[:3]
            axes.plot([origin_point[0], child_point[0]], [origin_point[1], child_point[1]], [origin_point[2], child_point[2]],
                      'k:', linewidth=0.6)
            if not joint.has_reference_child(child.title):
                origin_points += self.plot(child, axes, child_matrix)
        return origin_points

    def update(self, *args):
        """
        Funktion wird bei Änderungen aufgerufen, z.B. bei dem Benutzen des "Apply"-Buttons
        :param *args: Platzhalter
        """
        # Speichern der aktuellen Achsenbegrenzung (damit die Zoomstufe übernommen wird)
        xlims = self.axes.get_xlim3d()
        ylims = self.axes.get_ylim3d()
        zlims = self.axes.get_zlim3d()
        # Löschen der aktuellen Darstellung im Plotter
        self.axes.clear()
        # Plotten der neuen Konfiguration
        self.plot(self.robot.root, self.axes, root=True)
        self.axes.grid(False)
        self.axes.set(xlim3d=(xlims), xlabel='x')
        self.axes.set(ylim3d=(ylims), ylabel='y')
        self.axes.set(zlim3d=(zlims), zlabel='z')
        plt.draw()
        #plt.show(block=False)

    def plotter_show(self):
        #plt.show(block=True)
        pass

    #def print_button_clicked(self, *args):
    #    """Funktion zum Überprüfen und Testen des Buttons"""
    #    print("button_clicked")

    def set_joint_and_update(self, *args):
        """
        Hier können manuelle Winkeländerungen angegeben werden.
        """
        self.robot.set_joint(args[0], args[1])
        #self.robot.set_joint("Alpha1-Gelenk", math.radians(20))
        # self.robot.set_joint("Beta1-Gelenk", math.radians(-20))
        # self.robot.set_joint("Beta2-Gelenk", math.radians(-20))

        # Falls es Referenzgelenke gibt, können die Winkel der Duplikate unabhängig geändert werden
        # self.robot.set_joint("Gamma1-Gelenk", math.radians(90), math.radians(90))

        # self.robot.set_joint("Leg-2_Beta-Joint", math.radians(20))
        # self.robot.set_joint("Leg-2_Gamma-Joint", math.radians(20))
        # self.robot.set_joint("Leg-3_Gamma-Joint", math.radians(40))
        self.update(None)

    def reset_joints_offsets_update(self, title, *args):
        #print(f"{title=}")
        self.robot.reset_joint_offsets(title=title)
        self.update(None)

    def plot_quader(self, trans_matrix):
        h = 0.5 * self.geometry_scaling

        # 1_1 Teilflaeche
        x_1_1 = [h, -h, h]
        y_1_1 = [h, -h, -h]
        z_1_1 = [h, h, h]

        # 1_2 Teilflaeche
        x_1_2 = [h, -h, -h]
        y_1_2 = [h, -h, h]
        z_1_2 = [h, h, h]

        # 2_1 teilflaeche
        x_2_1 = [h, -h, h]
        y_2_1 = [h, -h, -h]
        z_2_1 = [-h, -h, -h]

        # 2_2 Teilflaeche
        x_2_2 = [h, -h, -h]
        y_2_2 = [h, -h, h]
        z_2_2 = [-h, -h, -h]

        # 3_1 Teilflaeche
        x_3_1 = [h, h, h]
        y_3_1 = [h, -h, h]
        z_3_1 = [h, -h, -h]

        # 3_2 Teilflaeche
        x_3_2 = [h, h, h]
        y_3_2 = [h, -h, -h]
        z_3_2 = [h, -h, h]

        # 4_1 Teilflaeche
        x_4_1 = [-h, -h, -h]
        y_4_1 = [h, -h, h]
        z_4_1 = [h, -h, -h]

        # 4_2 Teilflaeche
        x_4_2 = [-h, -h, -h]
        y_4_2 = [h, -h, -h]
        z_4_2 = [h, -h, h]

        # 5_1 Teilflaeche
        x_5_1 = [-h, h, h]
        y_5_1 = [h, h, h]
        z_5_1 = [h, -h, h]

        # 5_2 Teilflaeche
        x_5_2 = [-h, h, -h]
        y_5_2 = [h, h, h]
        z_5_2 = [h, -h, -h]

        # 6_1 Teilflaeche
        x_6_1 = [-h, h, h]
        y_6_1 = [-h, -h, -h]
        z_6_1 = [h, -h, h]

        # 6_2 Teilflaeche
        x_6_2 = [-h, h, -h]
        y_6_2 = [-h, -h, -h]
        z_6_2 = [h, -h, -h]

        # 7_1 Teilflaeche
        x_7_1 = [h, -h, h]
        y_7_1 = [h, -h, -h]
        z_7_1 = [1.2 * h, 1.2 * h, 1.2 * h]

        # 7_2 Teilflaeche
        x_7_2 = [h, -h, -h]
        y_7_2 = [h, -h, h]
        z_7_2 = [1.2 * h, 1.2 * h, 1.2 * h]

        self.plot_triangle(trans_matrix, x_1_1, y_1_1, z_1_1, 0.5, None)
        self.plot_triangle(trans_matrix, x_1_2, y_1_2, z_1_2, 0.5, None)
        self.plot_triangle(trans_matrix, x_2_1, y_2_1, z_2_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_2_2, y_2_2, z_2_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_3_1, y_3_1, z_3_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_3_2, y_3_2, z_3_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_4_1, y_4_1, z_4_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_4_2, y_4_2, z_4_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_5_1, y_5_1, z_5_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_5_2, y_5_2, z_5_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_6_1, y_6_1, z_6_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_6_2, y_6_2, z_6_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_7_1, y_7_1, z_7_1, 0.5, None)
        self.plot_triangle(trans_matrix, x_7_2, y_7_2, z_7_2, 0.5, None)

    def plot_cylinder(self, trans_matrix):
        #print(f"in plot cylinder: {self.geometry_scaling=}")
        r = 0.6 * self.geometry_scaling
        h = 0.8 * self.geometry_scaling
        t = 5
        p = 1.05

        # Pfeil_1_1_1
        x_p_1_1_1 = [(p * r), (math.sqrt(2) / 2) * (p * r), (p * r)]
        y_p_1_1_1 = [0, (math.sqrt(2) / 2) * (p * r), 0]
        z_p_1_1_1 = [h / t, -h / t, -h / t]

        # Pfeil_1_1_2
        x_p_1_1_2 = [(p * r), (math.sqrt(2) / 2) * (p * r), (math.sqrt(2) / 2) * (p * r)]
        y_p_1_1_2 = [0, (math.sqrt(2) / 2) * (p * r), (math.sqrt(2) / 2) * (p * r)]
        z_p_1_1_2 = [h / t, -h / t, h / t]

        # Pfeil_1_2_1
        x_p_1_2_1 = [(math.sqrt(2) / 2) * (p * r), 0, (math.sqrt(2) / 2) * (p * r)]
        y_p_1_2_1 = [(math.sqrt(2) / 2) * (p * r), (p * r), (math.sqrt(2) / 2) * (p * r)]
        z_p_1_2_1 = [h / t, -h / t, -h / t]

        # Pfeil_1_2_2
        x_p_1_2_2 = [(math.sqrt(2) / 2) * (p * r), 0, 0]
        y_p_1_2_2 = [(math.sqrt(2) / 2) * (p * r), (p * r), (p * r)]
        z_p_1_2_2 = [h / t, -h / t, h / t]

        # Pfeilspitze_1
        x_ps_1 = [0, 0, -(math.sqrt(2) / 2) * (p * r)]
        y_ps_1 = [(p * r), (p * r), (math.sqrt(2) / 2) * (p * r)]
        z_ps_1 = [2 * (h / t), -2 * (h / t), 0]

        # 1_1. Teilseitenflaeche
        x_1_1 = [0, 0, (math.sqrt(2) / 2) * r]
        y_1_1 = [r, r, (math.sqrt(2) / 2) * r]
        z_1_1 = [-h, h, -h]

        # 1_2. Teilseitenflaeche
        x_1_2 = [0, (math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r]
        y_1_2 = [r, (math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r]
        z_1_2 = [h, -h, h]

        # 2_1. Teilseitenflaeche
        x_2_1 = [(math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r, r]
        y_2_1 = [(math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r, 0]
        z_2_1 = [-h, h, -h]

        # 2_2. Teilseitenflaeche
        x_2_2 = [(math.sqrt(2) / 2) * r, r, r]
        y_2_2 = [(math.sqrt(2) / 2) * r, 0, 0]
        z_2_2 = [h, -h, h]

        # 3_1. Teilseitenflaeche
        x_3_1 = [r, r, (math.sqrt(2) / 2) * r]
        y_3_1 = [0, 0, -(math.sqrt(2) / 2) * r]
        z_3_1 = [-h, h, -h]

        # 3_2. Teilseitenflaeche
        x_3_2 = [r, (math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r]
        y_3_2 = [0,  -(math.sqrt(2) / 2) * r,  -(math.sqrt(2) / 2) * r]
        z_3_2 = [h, -h, h]

        # 4_1. Teilseitenflaeche
        x_4_1 = [(math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r, 0]
        y_4_1 = [-(math.sqrt(2) / 2) * r, -(math.sqrt(2) / 2) * r, -r]
        z_4_1 = [-h, h, -h]

        # 4_2. Teilseitenflaeche
        x_4_2 = [(math.sqrt(2) / 2) * r, 0, 0]
        y_4_2 = [-(math.sqrt(2) / 2) * r, -r, -r]
        z_4_2 = [h, -h, h]

        # 5_1. Teilseitenflaeche
        x_5_1 = [0, 0, -(math.sqrt(2) / 2) * r]
        y_5_1 = [-r, -r, -(math.sqrt(2) / 2) * r]
        z_5_1 = [-h, h, -h]

        # 5_2. Teilseitenflaeche
        x_5_2 = [0, -(math.sqrt(2) / 2) * r, -(math.sqrt(2) / 2) * r]
        y_5_2 = [-r, -(math.sqrt(2) / 2) * r, -(math.sqrt(2) / 2) * r]
        z_5_2 = [h, -h, h]

        # 6_1. Teilseitenflaeche
        x_6_1 = [-(math.sqrt(2) / 2) * r, -(math.sqrt(2) / 2) * r, -r]
        y_6_1 = [-(math.sqrt(2) / 2) * r, -(math.sqrt(2) / 2) * r, 0]
        z_6_1 = [-h, h, -h]

        # 6_2. Teilseitenflaeche
        x_6_2 = [-(math.sqrt(2) / 2) * r, -r, -r]
        y_6_2 = [-(math.sqrt(2) / 2) * r, 0, 0]
        z_6_2 = [h, -h, h]

        # 7_1. Teilseitenflaeche
        x_7_1 = [-r, -r, -(math.sqrt(2) / 2) * r]
        y_7_1 = [0, 0, (math.sqrt(2) / 2) * r]
        z_7_1 = [-h, h, -h]

        # 7_2. Teilseitenflaeche
        x_7_2 = [-r, -(math.sqrt(2) / 2) * r, -(math.sqrt(2) / 2) * r]
        y_7_2 = [0, (math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r]
        z_7_2 = [h, -h, h]

        # 8_1. Teilseitenflaeche
        x_8_1 = [-(math.sqrt(2) / 2) * r, -(math.sqrt(2) / 2) * r, 0]
        y_8_1 = [(math.sqrt(2) / 2) * r, (math.sqrt(2) / 2) * r, r]
        z_8_1 = [-h, h, -h]

        # 8_2. Teilseitenflaeche
        x_8_2 = [-(math.sqrt(2) / 2) * r, 0, 0]
        y_8_2 = [(math.sqrt(2) / 2) * r, r, r]
        z_8_2 = [h, -h, h]

        # 1_oben. Teildeckelflaeche
        x_1_o = [0, 0, (math.sqrt(2) / 2) * r]
        y_1_o = [0, r, (math.sqrt(2) / 2) * r]
        z_1_o = [h, h, h]

        # 2_oben. Teildeckelflaeche
        x_2_o = [0, (math.sqrt(2) / 2) * r, r]
        y_2_o = [0, (math.sqrt(2) / 2) * r, 0]
        z_2_o = [h, h, h]

        # 3_oben. Teildeckelflaeche
        x_3_o = [0, r, (math.sqrt(2) / 2) * r]
        y_3_o = [0, 0, -(math.sqrt(2) / 2) * r]
        z_3_o = [h, h, h]

        # 4_oben. Teildeckelflaeche
        x_4_o = [0, (math.sqrt(2) / 2) * r, 0]
        y_4_o = [0, -(math.sqrt(2) / 2) * r, -r]
        z_4_o = [h, h, h]


        # 5_oben. Teildeckelflaeche
        x_5_o = [0, 0, -(math.sqrt(2) / 2) * r]
        y_5_o = [0, -r, -(math.sqrt(2) / 2) * r]
        z_5_o = [h, h, h]

        # 6_oben. Teildeckelflaeche
        x_6_o = [0, -(math.sqrt(2) / 2) * r, -r]
        y_6_o = [0, -(math.sqrt(2) / 2) * r, 0]
        z_6_o = [h, h, h]

        # 7_oben. Teildeckelflaeche
        x_7_o = [0, -r, -(math.sqrt(2) / 2) * r]
        y_7_o = [0, 0, (math.sqrt(2) / 2) * r]
        z_7_o = [h, h, h]

        # 8_oben. Teildeckelflaeche
        x_8_o = [0, -(math.sqrt(2) / 2) * r, 0]
        y_8_o = [0, (math.sqrt(2) / 2) * r, r]
        z_8_o = [h, h, h]

        # 1_unten. Teildeckelflaeche
        x_1_u = [0, 0, (math.sqrt(2) / 2) * r]
        y_1_u = [0, r, (math.sqrt(2) / 2) * r]
        z_1_u = [-h, -h, -h]

        # 2_unten. Teildeckelflaeche
        x_2_u = [0, (math.sqrt(2) / 2) * r, r]
        y_2_u = [0, (math.sqrt(2) / 2) * r, 0]
        z_2_u = [-h, -h, -h]

        # 3_unten. Teildeckelflaeche
        x_3_u = [0, r, (math.sqrt(2) / 2) * r]
        y_3_u = [0, 0, -(math.sqrt(2) / 2) * r]
        z_3_u = [-h, -h, -h]

        # 4_unten. Teildeckelflaeche
        x_4_u = [0, (math.sqrt(2) / 2) * r, 0]
        y_4_u = [0, -(math.sqrt(2) / 2) * r, -r]
        z_4_u = [-h, -h, -h]

        # 5_unten. Teildeckelflaeche
        x_5_u = [0, 0, -(math.sqrt(2) / 2) * r]
        y_5_u = [0, -r, -(math.sqrt(2) / 2) * r]
        z_5_u = [-h, -h, -h]

        # 6_unten. Teildeckelflaeche
        x_6_u = [0, -(math.sqrt(2) / 2) * r, -r]
        y_6_u = [0, -(math.sqrt(2) / 2) * r, 0]
        z_6_u = [-h, -h, -h]

        # 7_unten. Teildeckelflaeche
        x_7_u = [0, -r, -(math.sqrt(2) / 2) * r]
        y_7_u = [0, 0, (math.sqrt(2) / 2) * r]
        z_7_u = [-h, -h, -h]

        # 8_unten. Teildeckelflaeche
        x_8_u = [0, -(math.sqrt(2) / 2) * r, 0]
        y_8_u = [0, (math.sqrt(2) / 2) * r, r]
        z_8_u = [-h, -h, -h]

        self.plot_triangle(trans_matrix, x_p_1_1_1, y_p_1_1_1, z_p_1_1_1, 1, None)
        self.plot_triangle(trans_matrix, x_p_1_1_2, y_p_1_1_2, z_p_1_1_2, 1, None)
        self.plot_triangle(trans_matrix, x_p_1_2_1, y_p_1_2_1, z_p_1_2_1, 1, None)
        self.plot_triangle(trans_matrix, x_p_1_2_2, y_p_1_2_2, z_p_1_2_2, 1, None)
        self.plot_triangle(trans_matrix, x_ps_1, y_ps_1, z_ps_1, 1, None)

        self.plot_triangle(trans_matrix, x_1_1, y_1_1, z_1_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_1_2, y_1_2, z_1_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_2_1, y_2_1, z_2_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_2_2, y_2_2, z_2_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_3_1, y_3_1, z_3_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_3_2, y_3_2, z_3_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_4_1, y_4_1, z_4_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_4_2, y_4_2, z_4_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_5_1, y_5_1, z_5_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_5_2, y_5_2, z_5_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_6_1, y_6_1, z_6_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_6_2, y_6_2, z_6_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_7_1, y_7_1, z_7_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_7_2, y_7_2, z_7_2, 0.2, None)
        self.plot_triangle(trans_matrix, x_8_1, y_8_1, z_8_1, 0.2, None)
        self.plot_triangle(trans_matrix, x_8_2, y_8_2, z_8_2, 0.2, None)

        self.plot_triangle(trans_matrix, x_1_o, y_1_o, z_1_o, 0.5, None)
        self.plot_triangle(trans_matrix, x_2_o, y_2_o, z_2_o, 0.5, None)
        self.plot_triangle(trans_matrix, x_3_o, y_3_o, z_3_o, 0.5, None)
        self.plot_triangle(trans_matrix, x_4_o, y_4_o, z_4_o, 0.5, None)
        self.plot_triangle(trans_matrix, x_5_o, y_5_o, z_5_o, 0.5, None)
        self.plot_triangle(trans_matrix, x_6_o, y_6_o, z_6_o, 0.5, None)
        self.plot_triangle(trans_matrix, x_7_o, y_7_o, z_7_o, 0.5, None)
        self.plot_triangle(trans_matrix, x_8_o, y_8_o, z_8_o, 0.5, None)

        self.plot_triangle(trans_matrix, x_1_u, y_1_u, z_1_u, 0.5, None)
        self.plot_triangle(trans_matrix, x_2_u, y_2_u, z_2_u, 0.5, None)
        self.plot_triangle(trans_matrix, x_3_u, y_3_u, z_3_u, 0.5, None)
        self.plot_triangle(trans_matrix, x_4_u, y_4_u, z_4_u, 0.5, None)
        self.plot_triangle(trans_matrix, x_5_u, y_5_u, z_5_u, 0.5, None)
        self.plot_triangle(trans_matrix, x_6_u, y_6_u, z_6_u, 0.5, None)
        self.plot_triangle(trans_matrix, x_7_u, y_7_u, z_7_u, 0.5, None)
        self.plot_triangle(trans_matrix, x_8_u, y_8_u, z_8_u, 0.5, None)

    def plot_triangle(self, trans_matrix, points_x: list, points_y: list, points_z: list, alpha, col: str):
        # Transformation zu homogenen Koordinaten und
        # Matrixmultiplikation von Transformationsmatrix mit Punkt
        vertices_1 = [np.dot(trans_matrix, [points_x[0], points_y[0], points_z[0], 1]),
                        np.dot(trans_matrix, [points_x[1], points_y[1], points_z[1], 1]),
                        np.dot(trans_matrix, [points_x[2], points_y[2], points_z[2], 1])]

        vertices_2 = [[[]] for i in range(3)]
        for point in range(3):
            vertices_2[point][0].append(vertices_1[point][0])
            vertices_2[point][0].append(vertices_1[point][1])
            vertices_2[point][0].append(vertices_1[point][2])
            vertices_1[point] = tuple(vertices_2[point][0])

        vertices_1 = [vertices_1]

        poly_1 = Poly3DCollection(vertices_1, alpha=alpha, facecolors=col)
        self.axes.add_collection3d(poly_1)

    def calc_limits(self, origin_points, padding = 0.1):
        stacked_origin_points = np.vstack(origin_points)
        x_min = min(stacked_origin_points[:, 0]) * (padding+1)
        x_max = max(stacked_origin_points[:, 0]) * (padding+1)
        y_min = min(stacked_origin_points[:, 1]) * (padding+1)
        y_max = max(stacked_origin_points[:, 1]) * (padding+1)
        z_min = min(stacked_origin_points[:, 2]) * (padding+1)
        z_max = max(stacked_origin_points[:, 2]) * (padding+1)
        minimum = min(x_min, y_min, z_min)
        maximum = max(x_max, y_max, z_max)
        return (minimum, maximum)

    def set_show_options(self, *args):
        self.show_title = args[0]
        self.show_name = args[1]
        self.show_3d_symbol = args[2]
        self.update(None)

    def apply_joint_change(self, *args):
        self.robot.set_joint(self.title_list[self.radio_joints.active], float(self.text_value.text))

    def generate_dh_matrix_from_to(self, _from, _to):
        matrix = self.robot.generate_dh_matrix_from_to(_from, _to)
        return matrix

    def calc_inverse_dh_matrix(self, trans_matrix):
        inverse_matrix = self.robot.calc_inverse_dh_matrix(trans_matrix)
        return inverse_matrix

    def get_joint_offsets(self, joint):
        return self.robot.get_joint_offsets(joint)