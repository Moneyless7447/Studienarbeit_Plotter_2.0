import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import robot
import plotter

'''
GUI class 
It contains attributes and methods to visualize a given "plotter" object and features 
to interact with it such as allowing inputs from a user to call specific functions from other classes.
'''
class GUI:
    def __init__(self):
        # INSERT JSON FILE HERE (no user input via GUI for this feature implemented yet)
        self.robot_json = "example_robot_hexapod.json"
        self.robot = robot.Robot("test_roboter", self.robot_json)
        self.fig = plt.figure(figsize=(7, 7), dpi=80, tight_layout=True)
        self.plotter = plotter.Plotter(self.robot, self.fig)
        self.window = tk.Tk()
        self.window.geometry('1800x1200')
        self.window.title("RoboPlot")

        #Default matrix, this attribute gets manipulated when
        #calculating transformation matrices when the user uses the corresponding method(s)
        self.transformationmatrix_A_B = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

        def on_close():
            self.window.destroy()
            exit(0)
        self.window.protocol("WM_DELETE_WINDOW", on_close)

        '''Visual settings and design elements'''
        self.label_node_selection = ttk.Label(self.window, text='Joint (title):')
        self.node_selection = ttk.Combobox(self.window, width=17)
        self.node_selection['values'] = self.robot.get_joint_titles()[1:]
        self.node_selection.set(self.node_selection['values'][0])

        self.input_text = tk.StringVar()
        self.label_value_input = ttk.Label(self.window, text='Value (deg or distance):')
        self.value_input = ttk.Entry(self.window, textvariable=self.input_text, width=20)

        self.apply_button = tk.Button(self.window, text='Apply', command=self.apply_changes, width=20)
        self.reset_button_img = tk.PhotoImage(file="reset_button.png", master=self.window)
        self.reset_button = tk.Button(self.window, image=self.reset_button_img, command=self.reset_changes, width=32,
                                      height=32)
        self.reset_all_button = tk.Button(self.window, text='Reset all', command=self.reset_all_changes, width=20)
        self.view = FigureCanvasTkAgg(self.fig, self.window)

        self.bool_title = True #Initinal value of the title checkbox
        self.check_title = tk.Checkbutton(self.window, text='Titles', command=self.toggle_title)
        self.check_title.select()
        self.bool_name = False #Initinal value of the name checkbox
        self.check_name = tk.Checkbutton(self.window, text='Names (generated)', command=self.toggle_name)
        self.check_name.deselect()
        self.bool_symbols = True #Initinal value of the 3D-symbol checkbox
        self.check_symbols = tk.Checkbutton(self.window, text='3D-Symbols', command=self.toggle_symbols)
        self.check_symbols.select()
        self.set_show_options()

        self.label_json = ttk.Label(self.window, text="JSON-File: ")
        self.json = ttk.Label(self.window, text=self.robot_json)
        self.label_hyphen = ttk.Label(self.window, text='______________________________________________________')
        self.label_headline = ttk.Label(self.window, text='Transformation Matrices from A to B')
        self.label_joint_A = ttk.Label(self.window, text='Joint A: ')
        self.label_joint_B = ttk.Label(self.window, text='Joint B: ')
        self.calculate_button_img = tk.PhotoImage(file='T_A_B.png', master=self.window)
        self.calculate_button = tk.Button(self.window, image=self.calculate_button_img, command=self.calculate_AtoB)
        self.node_selection_A = ttk.Combobox(self.window, width=17)
        self.node_selection_A['values'] = self.robot.get_joint_titles()[1:]
        self.node_selection_A.set(self.node_selection_A['values'][0])
        self.node_selection_B = ttk.Combobox(self.window, width=17)
        self.node_selection_B['values'] = self.robot.get_joint_titles()[1:]
        self.node_selection_B.set(self.node_selection_B['values'][0])
        self.scrollbar_transformationmatrix = tk.Scrollbar(self.window)
        self.node_transformationmatrix_A_B = tk.Text(self.window, width=36, height=16, yscrollcommand=self.scrollbar_transformationmatrix.set, padx=2, pady=7)
        self.node_transformationmatrix_A_B.insert(tk.END, "┌          ┐\n|┌     ┐┌ ┐|  R is the 3x3 R_A_B\n"
                                                          "|          |  "
                                                          "rotation matrix.\n|   R    V |\n|          |  "
                                                          "V is the 3x1 V_B\n|└     ┘└ ┘|  translation vector.\n"
                                                          "| 0 0 0  1 |\n└          ┘\n┌          ┐\n|┌     ┐┌ ┐|  "
                                                          "This transformation\n| 1 0 0  0 |  matrix equals a\n"
                                                          "| 0 1 0  0 |  transformation with\n| 0 0 1  0 |  "
                                                          "no rotation\n|└     ┘└ ┘|  nor translation.\n| 0 0 0  1 |"
                                                          "\n└          ┘") #Initial input for the output text field
        self.scrollbar_transformationmatrix.config(command=self.node_transformationmatrix_A_B.yview)
        self.geometry_scale = tk.Scale(self.window, from_=1, to=10, orient='horizontal', command=self.set_geometry_scaling_factor, resolution=0.5, length=300, width=30)
        self.geometry_scale.set(self.plotter.get_geometry_scaling_factor())

        '''Positioning of the visual elements on the GUI grid'''
        self.label_json.grid(column=1, columnspan=1, row=1, sticky='w', rowspan=2, padx=10, pady=20)
        self.json.grid(column=1, columnspan=3, row=1, sticky='w', rowspan=2, padx=130)
        self.label_node_selection.grid(column=1, row=10, padx=10, pady=1, sticky='w')
        self.node_selection.grid(column=3, row=10, padx=3, pady=5, sticky='w')
        self.label_value_input.grid(columnspan=2, column=1, row=11, padx=10, pady=5, sticky='w')
        self.value_input.grid(column=3, row=11, padx=2, pady=5, sticky='w')
        self.apply_button.grid(column=3, row=12, padx=2, pady=5, sticky='w')
        self.reset_button.grid(column=1, columnspan=2, row=10, padx=10, pady=5, sticky='e')
        self.reset_all_button.grid(column=1, columnspan=2, row=12, padx=2, pady=5, sticky='w')
        self.view.get_tk_widget().grid(columnspan=4, rowspan=40, row=1, column=4, padx=20, pady=10, sticky='w')
        self.check_name.grid(column=1, row=3, sticky='w', padx=10, columnspan=2)
        self.check_title.grid(column=1, row=4, sticky='w', padx=10)
        self.check_symbols.grid(column=1, row=5, sticky='w', padx=10)
        self.geometry_scale.grid(column=2, row=4, sticky='nw', padx=0, pady=50, columnspan=2, rowspan=4)
        self.label_hyphen.grid(column=1, columnspan=3, row=15, padx=1, pady=1, sticky='n')
        self.label_headline.grid(column=1, columnspan=3, row=16, padx=1, pady=1, sticky='n')
        self.label_joint_A.grid(column=2, row=17, padx=1, pady=1, sticky='w')
        self.label_joint_B.grid(column=2, row=18, padx=1, pady=1, sticky='w')
        self.calculate_button.grid(column=1, row=17, padx=20, pady=1, sticky='we', columnspan=1, rowspan=2)
        self.node_selection_A.grid(column=3, columnspan=1, row=17, padx=1, pady=1, sticky='w')
        self.node_selection_B.grid(column=3, columnspan=1, row=18, padx=1, pady=1, sticky='w')
        self.node_transformationmatrix_A_B.grid(column=1, row=19, sticky='nw', columnspan=3, padx=20)
        self.scrollbar_transformationmatrix.grid(column=3, row=19, sticky='ns', rowspan=3, columnspan=2, padx=1)


    def set_geometry_scaling_factor(self, *args):
        factor = self.geometry_scale.get()
        self.plotter.set_geometry_scaling_factor(factor)

    #apply user input changes for a selected joint
    def apply_changes(self):
        # print(self.value_input.get())
        self.plotter.set_joint_and_update(self.node_selection.get(), self.value_input.get().split(','))

    def reset_all_changes(self):
        ''' Resets all changes which were applied by a user via
        Setzt die Veränderungen durch Eingaben in dem Eingabefenster für alle Gelenke (Joints) zurück.
        '''
        titles = self.robot.get_joint_titles()[0:]
        # self.node_selection['values'] = self.robot.get_joint_titles()[1:]
        for title in titles:
            self.plotter.reset_joints_offsets_update(title)

    def reset_changes(self):
        '''
        Setzt die Veränderungen durch Eingaben in dem Eingabefenster für ein spezifisches Gelenk (Joint) zurück.
        :return:
        '''
        #print("Trying to reset specific joint:")
        #print(f"nodeselection: {self.node_selection.get()=}")
        #print(f"TEST: {self.plotter.get_joint_offsets(self.node_selection.get())}")
        self.plotter.reset_joints_offsets_update(self.node_selection.get())
        #print("reached end")

    def set_show_options(self):
        # print(self.bool_title, self.bool_name, self.bool_symbols)
        self.plotter.set_show_options(self.bool_title, self.bool_name, self.bool_symbols)
        # self.plotter.set_show_options(self.bool_title.get(), self.bool_name.get(), self.bool_symbols.get())

    def toggle_title(self):
        self.bool_title = not self.bool_title
        # self.check_title.select() if self.bool_title else self.check_title.deselect()
        self.set_show_options()

    def toggle_name(self):
        self.bool_name = not self.bool_name
        # self.check_name.select() if self.bool_name else self.check_name.deselect()
        self.set_show_options()

    def toggle_symbols(self):
        self.bool_symbols = not self.bool_symbols
        # self.check_symbols.select() if self.bool_symbols else self.check_symbols.deselect()

        if not self.bool_symbols:
            self.geometry_scale.config(state=tk.DISABLED, takefocus=0, fg='lightgrey')
        else:
            self.geometry_scale.config(state=tk.ACTIVE, takefocus=1, fg='black')
        self.set_show_options()

    @staticmethod
    def strip_matrix_string(matrix):
        '''
        Zerlegt und formatiert eine Matrix um sie mit Klammern in dem Dialogfenster anzeigen lassen zu können.
        '''
        lines = str(matrix).split("\n")
        res = []
        for line in lines:
            res.append("|"+line.lstrip().rstrip().replace("[", "").replace("]", "")+"|")

        res.insert(0, "┌"+" "* (len(res[0])-2)+"┐")
        res.append("└" + " " * (len(res[0])-2) + "┘")
        return "\n".join(res)

    def calculate_AtoB(self):
        '''
        Berechnet die Transformationsmatrix von einem Gelenk zu einem anderen, nutzt dafür die Auswahl der Gelenke in der GUI.
        :return:
        '''
        if self.node_selection_A.get() == self.node_selection_B.get():
            a_to_b = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
            self.node_transformationmatrix_A_B.insert(tk.END,
                                                      f"\n\nT_{self.node_selection_A.get()}_{self.node_selection_B.get()}:\n")
            self.node_transformationmatrix_A_B.insert(tk.END, self.strip_matrix_string(a_to_b))
            self.node_transformationmatrix_A_B.insert(tk.END, "\n\n\n\n\n\n\n\n\n")
            self.node_transformationmatrix_A_B.see(tk.END)
        else:
            try:
                a_to_b = self.plotter.generate_dh_matrix_from_to(self.node_selection_A.get(),
                                                                 self.node_selection_B.get())
                for i in range(4):
                    for j in range(4):
                        a_to_b[i][j] = round(a_to_b[i][j], 2)
                self.node_transformationmatrix_A_B.insert(tk.END,
                                                          f"\n\nT_{self.node_selection_A.get()}_{self.node_selection_B.get()}:\n")
                self.node_transformationmatrix_A_B.insert(tk.END, self.strip_matrix_string(a_to_b))
                self.node_transformationmatrix_A_B.insert(tk.END, "\n\n\n\n\n\n\n\n\n")
                self.node_transformationmatrix_A_B.see(tk.END)
            except TypeError:
                try:
                    b_to_a = self.plotter.generate_dh_matrix_from_to(self.node_selection_B.get(),
                                                                     self.node_selection_A.get())
                    for i in range(4):
                        for j in range(4):
                            b_to_a[i][j] = round(b_to_a[i][j], 2)
                    self.node_transformationmatrix_A_B.insert(tk.END,
                                                              f"\n\nT_A_B is not directly\ncalculatable, instead:\nT_{self.node_selection_B.get()}_{self.node_selection_A.get()}:\n")
                    self.node_transformationmatrix_A_B.insert(tk.END, self.strip_matrix_string(b_to_a))
                    self.node_transformationmatrix_A_B.insert(tk.END, "\nCalculated inverse (T_A_B):\n")
                    a_to_b = self.plotter.calc_inverse_dh_matrix(b_to_a)
                    self.node_transformationmatrix_A_B.insert(tk.END, self.strip_matrix_string(a_to_b))
                    self.node_transformationmatrix_A_B.see(tk.END)
                except TypeError:
                    self.node_transformationmatrix_A_B.insert(tk.END,
                                                              f"\n\nNot calculatable in this\nversion, maybe there is no\ndirect kinetic chain between\nthose two joints\nor the program can not find\nthe path from one joint to another.\n\n\n\n\n\n\n\n\n")
                    self.node_transformationmatrix_A_B.see(tk.END)


if __name__ == '__main__':
    gui = GUI()
    gui.window.mainloop()
