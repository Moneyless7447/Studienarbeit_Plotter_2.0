import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import robot
import plotter


class GUI:
    def __init__(self):
        self.robot = robot.Robot("test_roboter", "example_robot_dh_linear.json")
        self.fig = plt.figure(figsize=(6, 6), dpi=80, tight_layout=True)
        self.plotter = plotter.Plotter(self.robot, self.fig)
        self.window = tk.Tk()
        self.window.geometry('800x500')
        self.window.configure(bg="white")
        self.window.title("RoboPlot")

        def on_close():
            self.window.destroy()
            exit(0)
        self.window.protocol("WM_DELETE_WINDOW", on_close)

        self.label_node_selection = ttk.Label(self.window, text='Joint:')#, background='#36373d', foreground='white')
        self.node_selection = ttk.Combobox(self.window, width=30)
        self.node_selection['values'] = self.robot.get_joint_titles()[1:]
        self.node_selection.set(self.node_selection['values'][0])

        self.input_text = tk.StringVar()
        self.label_value_input = ttk.Label(self.window, text='Value (deg):')#, background='#36373d', foreground='white')
        self.value_input = ttk.Entry(self.window, textvariable=self.input_text, width=33)

        self.apply_button = tk.Button(self.window, text='Apply', command=self.apply_changes, bg='#76798a', fg='white',
                                      width=28)
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

        self.label_node_selection.grid(column=1, row=9, padx=2, pady=1, sticky='w')
        self.node_selection.grid(column=2, row=9, padx=2, pady=5, sticky='w')
        self.label_value_input.grid(column=1, row=10, padx=2, pady=5, sticky='w')
        self.value_input.grid(column=2, row=10, padx=2, pady=1, sticky='w')
        self.apply_button.grid(column=2, row=11, padx=2, pady=5, sticky='w')
        self.view.get_tk_widget().grid(columnspan=1, rowspan=40, row=1, column=3, padx=10, pady=10)
        self.check_name.grid(column=1, row=2, sticky='w')
        self.check_title.grid(column=1, row=3, sticky='w')
        self.check_symbols.grid(column=1, row=4, sticky='w')

    def apply_changes(self):
        # print(self.value_input.get())
        self.plotter.set_joint_and_update(self.node_selection.get(), self.value_input.get().split(','))

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


if __name__ == '__main__':
    gui = GUI()
    gui.window.mainloop()
