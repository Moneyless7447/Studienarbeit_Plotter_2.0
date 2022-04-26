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
        self.robot = robot.Robot("test_roboter", "example_robot_dh_linear.json")
        self.fig = plt.figure(figsize=(6, 6), dpi=80, tight_layout=True)
        self.plotter = plotter.Plotter(self.robot, self.fig)
        self.window = tk.Tk()
        self.window.geometry('800x500')
        #self.window.configure(bg="white")
        self.window.title("RoboPlot")
        self.transformationmatrix_A_B = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])

        def on_close():
            self.window.destroy()
            exit(0)
        self.window.protocol("WM_DELETE_WINDOW", on_close)

        self.label_node_selection = ttk.Label(self.window, text='Joint (title):')#, background='#36373d', foreground='white')
        self.node_selection = ttk.Combobox(self.window, width=17)
        self.node_selection['values'] = self.robot.get_joint_titles()[1:]
        self.node_selection.set(self.node_selection['values'][0])

        self.input_text = tk.StringVar()
        self.label_value_input = ttk.Label(self.window, text='Value (deg or distance):')#, background='#36373d', foreground='white')
        self.value_input = ttk.Entry(self.window, textvariable=self.input_text, width=20)

        # self.apply_button = tk.Button(self.window, text='Apply', command=self.apply_changes, bg='#76798a', fg='white',
        #                               width=28)
        self.apply_button = tk.Button(self.window, text='Apply', command=self.apply_changes, width=20)
        self.reset_button_img = tk.PhotoImage(file="reset_button.png", master=self.window)
        self.reset_button = tk.Button(self.window, image=self.reset_button_img, command=self.reset_changes, width=32, height=32)
        self.reset_all_button = tk.Button(self.window, text='Reset all', command=self.reset_all_changes, width=20)
        self.view = FigureCanvasTkAgg(self.fig, self.window)


        self.bool_title = True
        # self.bool_title.set(0)
        self.check_title = tk.Checkbutton(self.window,
                                          text='Titles',
                                          command=self.toggle_title)#,
                                          # background='#36373d', foreground='white')
        self.check_title.select()
        self.bool_name = False
        # self.bool_name.set(0)
        self.check_name = tk.Checkbutton(self.window, text='Name', command=self.toggle_name)#, background='#36373d',
                                         # foreground='white')
        self.check_name.deselect()
        self.bool_symbols = True
        # self.bool_symbols.set(0)
        self.check_symbols = tk.Checkbutton(self.window, text='3D-Symbols', command=self.toggle_symbols)#,
                                            # background='#36373d', foreground='white')
        self.check_symbols.select()
        self.set_show_options()

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
        self.node_transformationmatrix_A_B = tk.Text(self.window, width=30, height=5, yscrollcommand=True, padx=2)
        self.node_transformationmatrix_A_B.insert(tk.END, self.transformationmatrix_A_B)

        self.label_node_selection.grid(column=1, row=9, padx=2, pady=1, sticky='w')
        self.node_selection.grid(column=3, row=9, padx=3, pady=5, sticky='w')
        self.label_value_input.grid(columnspan=2, column=1, row=10, padx=1, pady=5, sticky='w')
        self.value_input.grid(column=3, row=10, padx=2, pady=5, sticky='w')
        self.apply_button.grid(column=3, row=11, padx=2, pady=5, sticky='w')
        self.reset_button.grid(column=1, columnspan=2, row=9, padx=1, pady=5, sticky='e')
        self.reset_all_button.grid(column=1, columnspan=2, row=11, padx=2, pady=5, sticky='w')
        self.view.get_tk_widget().grid(columnspan=1, rowspan=40, row=1, column=4, padx=10, pady=10)
        self.check_name.grid(column=1, row=2, sticky='w')
        self.check_title.grid(column=1, row=3, sticky='w')
        self.check_symbols.grid(column=1, row=4, sticky='w')
        self.label_hyphen.grid(column=1, columnspan=3, row=14, padx=1, pady=1, sticky='n')
        self.label_headline.grid(column=1, columnspan=3, row=15, padx=1, pady=1, sticky='n')
        self.label_joint_A.grid(column=2, row=16, padx=1, pady=1, sticky='w')
        self.label_joint_B.grid(column=2, row=17, padx=1, pady=1, sticky='w')
        self.calculate_button.grid(column=1, row=16, padx=20, pady=1, sticky='w', columnspan=2, rowspan=2)
        self.node_selection_A.grid(column=3, columnspan=1, row=16, padx=1, pady=1, sticky='w')
        self.node_selection_B.grid(column=3, columnspan=1, row=17, padx=1, pady=1, sticky='w')
        self.node_transformationmatrix_A_B.grid(column=1, row=18, sticky='n', columnspan=3)

    def apply_changes(self):
        # print(self.value_input.get())
        self.plotter.set_joint_and_update(self.node_selection.get(), self.value_input.get().split(','))

    def reset_all_changes(self):
        titles = self.robot.get_joint_titles()[1:]
        #self.node_selection['values'] = self.robot.get_joint_titles()[1:]
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

    def calculate_AtoB(self):
        if self.node_selection_A.get() == self.node_selection_B.get():
            a_to_b = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
        else:
            a_to_b = self.plotter.generate_dh_matrix_from_to(self.node_selection_A.get(), self.node_selection_B.get())
            for i in range(3):
                for j in range(3):
                    a_to_b[i][j] = round(a_to_b[i][j], 2)
        print(f"Matrix from A to B: \n{a_to_b}")
        print(f"test: \n{a_to_b[0][0]}")
        #self.node_transformationmatrix_A_B.delete(tk.FIRST, tk.LAST)
        self.node_transformationmatrix_A_B.insert(tk.END, f"\nT_{self.node_selection_A.get()}_{self.node_selection_B.get()}:\n")
        self.node_transformationmatrix_A_B.insert(tk.END, a_to_b)
        self.node_transformationmatrix_A_B.see(tk.END)


if __name__ == '__main__':
    gui = GUI()
    gui.window.mainloop()
