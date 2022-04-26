import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

import robot
import plotter


class GUI:
    def __init__(self):
        self.robot_json = "example_robot_dh_linear_2.json"
        self.robot = robot.Robot("test_roboter", self.robot_json)
        self.fig = plt.figure(figsize=(6, 6), dpi=80, tight_layout=True)
        self.plotter = plotter.Plotter(self.robot, self.fig)
        self.window = tk.Tk()
        self.window.geometry('800x500')
        # self.window.configure(bg="white")
        self.window.title("RoboPlot")
        self.transformationmatrix_A_B = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

        def on_close():
            self.window.destroy()
            exit(0)

        self.window.protocol("WM_DELETE_WINDOW", on_close)

        self.label_node_selection = ttk.Label(self.window,
                                              text='Joint (title):')  # , background='#36373d', foreground='white')
        self.node_selection = ttk.Combobox(self.window, width=17)
        self.node_selection['values'] = self.robot.get_joint_titles()[1:]
        self.node_selection.set(self.node_selection['values'][0])

        self.input_text = tk.StringVar()
        self.label_value_input = ttk.Label(self.window,
                                           text='Value (deg or distance):')  # , background='#36373d', foreground='white')
        self.value_input = ttk.Entry(self.window, textvariable=self.input_text, width=20)

        # self.apply_button = tk.Button(self.window, text='Apply', command=self.apply_changes, bg='#76798a', fg='white',
        #                               width=28)
        self.apply_button = tk.Button(self.window, text='Apply', command=self.apply_changes, width=20)
        self.reset_button_img = tk.PhotoImage(file="reset_button.png", master=self.window)
        self.reset_button = tk.Button(self.window, image=self.reset_button_img, command=self.reset_changes, width=32,
                                      height=32)
        self.reset_all_button = tk.Button(self.window, text='Reset all', command=self.reset_all_changes, width=20)
        self.view = FigureCanvasTkAgg(self.fig, self.window)

        self.bool_title = True
        # self.bool_title.set(0)
        self.check_title = tk.Checkbutton(self.window,
                                          text='Titles',
                                          command=self.toggle_title)  # ,
        # background='#36373d', foreground='white')
        self.check_title.select()
        self.bool_name = False
        # self.bool_name.set(0)
        self.check_name = tk.Checkbutton(self.window, text='Name', command=self.toggle_name)  # , background='#36373d',
        # foreground='white')
        self.check_name.deselect()
        self.bool_symbols = True
        # self.bool_symbols.set(0)
        self.check_symbols = tk.Checkbutton(self.window, text='3D-Symbols', command=self.toggle_symbols)  # ,
        # background='#36373d', foreground='white')
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
        self.node_transformationmatrix_A_B = tk.Text(self.window, width=33, height=15, yscrollcommand=self.scrollbar_transformationmatrix.set, padx=2, pady=7)
        self.node_transformationmatrix_A_B.insert(tk.END, self.strip_matrix_string(self.transformationmatrix_A_B))
        self.scrollbar_transformationmatrix.config(command=self.node_transformationmatrix_A_B.yview)




        self.label_json.grid(column=1, columnspan=1, row=1, sticky='w', rowspan=2, padx=10)
        self.json.grid(column=1, columnspan=3, row=1, sticky='w', rowspan=2, padx=130)
        self.label_node_selection.grid(column=1, row=10, padx=10, pady=1, sticky='w')
        self.node_selection.grid(column=3, row=10, padx=3, pady=5, sticky='w')
        self.label_value_input.grid(columnspan=2, column=1, row=11, padx=10, pady=5, sticky='w')
        self.value_input.grid(column=3, row=11, padx=2, pady=5, sticky='w')
        self.apply_button.grid(column=3, row=12, padx=2, pady=5, sticky='w')
        self.reset_button.grid(column=1, columnspan=2, row=10, padx=10, pady=5, sticky='e')
        self.reset_all_button.grid(column=1, columnspan=2, row=12, padx=2, pady=5, sticky='w')
        self.view.get_tk_widget().grid(columnspan=4, rowspan=40, row=2, column=4, padx=10, pady=10, sticky='w')
        self.check_name.grid(column=1, row=3, sticky='w', padx=10)
        self.check_title.grid(column=1, row=4, sticky='w', padx=10)
        self.check_symbols.grid(column=1, row=5, sticky='w', padx=10)
        self.label_hyphen.grid(column=1, columnspan=3, row=15, padx=1, pady=1, sticky='n')
        self.label_headline.grid(column=1, columnspan=3, row=16, padx=1, pady=1, sticky='n')
        self.label_joint_A.grid(column=2, row=17, padx=1, pady=1, sticky='w')
        self.label_joint_B.grid(column=2, row=18, padx=1, pady=1, sticky='w')
        self.calculate_button.grid(column=1, row=17, padx=20, pady=1, sticky='we', columnspan=2, rowspan=2)
        self.node_selection_A.grid(column=3, columnspan=1, row=17, padx=1, pady=1, sticky='w')
        self.node_selection_B.grid(column=3, columnspan=1, row=18, padx=1, pady=1, sticky='w')
        self.node_transformationmatrix_A_B.grid(column=1, row=19, sticky='nw', columnspan=3, padx=20)
        self.scrollbar_transformationmatrix.grid(column=3, row=19, sticky='ns', rowspan=3, columnspan=2, padx=1)

    def apply_changes(self):
        # print(self.value_input.get())
        self.plotter.set_joint_and_update(self.node_selection.get(), self.value_input.get().split(','))

    def reset_all_changes(self):
        titles = self.robot.get_joint_titles()[1:]
        # self.node_selection['values'] = self.robot.get_joint_titles()[1:]
        for title in titles:
            self.plotter.reset_joints_offsets_update(titles)

    def reset_changes(self):

        print("hiiiiiiiier")
        print(f"nodeselection: {self.node_selection.get()}")
        self.plotter.reset_joints_offsets_update(self.node_selection.get())
        print("342214")

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
        self.set_show_options()

    @staticmethod
    def strip_matrix_string(matrix):
        lines = str(matrix).split("\n")
        res = []
        for line in lines:
            res.append("|"+line.lstrip().rstrip().replace("[", "").replace("]", "")+"|")

        res.insert(0, "┌"+" "* (len(res[0])-2)+"┐")
        res.append("└" + " " * (len(res[0])-2) + "┘")
        return "\n".join(res)

    def calculate_AtoB(self):
        if self.node_selection_A.get() == self.node_selection_B.get():
            a_to_b = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
            self.node_transformationmatrix_A_B.insert(tk.END,
                                                      f"\n\nT_{self.node_selection_A.get()}_{self.node_selection_B.get()}:\n")
            self.node_transformationmatrix_A_B.insert(tk.END, self.strip_matrix_string(a_to_b))
            self.node_transformationmatrix_A_B.insert(tk.END, "\n\n\n\n\n\n\n\n")
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
                self.node_transformationmatrix_A_B.insert(tk.END, "\n\n\n\n\n\n\n\n")
                self.node_transformationmatrix_A_B.see(tk.END)
            except TypeError:
                try:
                    a_to_b = self.plotter.generate_dh_matrix_from_to(self.node_selection_B.get(),
                                                                     self.node_selection_A.get())
                    for i in range(4):
                        for j in range(4):
                            a_to_b[i][j] = round(a_to_b[i][j], 2)
                    self.node_transformationmatrix_A_B.insert(tk.END,
                                                              f"\n\nT_A_B is not directly\ncalculatable, instead:\nT_{self.node_selection_B.get()}_{self.node_selection_A.get()}:\n")
                    self.node_transformationmatrix_A_B.insert(tk.END, self.strip_matrix_string(a_to_b))
                    self.node_transformationmatrix_A_B.insert(tk.END, "\nCalculated inverse (T_A_B):")
                    # inverse?
                    self.node_transformationmatrix_A_B.see(tk.END)
                except TypeError:
                    self.node_transformationmatrix_A_B.insert(tk.END,
                                                              f"\n\nNot calculatable in this\nversion, maybe there is no\ndirect kinetic chain between\nthose two joints.\n\n\n\n\n\n\n\n\n\n\n")
                    self.node_transformationmatrix_A_B.see(tk.END)


if __name__ == '__main__':
    gui = GUI()
    gui.window.mainloop()
