import tkinter as tk
from tkinter import ttk
import robot
import plotter


class GUI:
    def __init__(self):
        self.robot = robot.Robot("test_roboter", "_extra_Kind.json")
        self.plotter = plotter.Plotter(self.robot)
        self.window = tk.Tk()
        self.window.geometry('400x300')
        self.label_node_selection = ttk.Label(self.window, text = 'Joint:')
        self.node_selection = ttk.Combobox(self.window)
        self.node_selection['values'] = self.robot.get_joint_titles()
        self.node_selection.set(self.node_selection['values'][0])
        self.input_text = tk.StringVar()
        self.label_value_input = ttk.Label(self.window, text='Value (deg):')
        self.value_input = ttk.Entry(self.window, textvariable=self.input_text)
        self.apply_button = ttk.Button(self.window, text='Apply', command=self.apply_changes)
        self.label_node_selection.grid(column=1, row=1, padx=2, pady=5, sticky='w')
        self.node_selection.grid(column=2, row=1, padx=2, pady=5, sticky='w')
        self.label_value_input.grid(column=1, row=2, padx=2, pady=5, sticky='w')
        self.value_input.grid(column=2, row=2, padx=2, pady=5,  sticky='w')
        self.apply_button.grid(column=2, row=3, padx=2, pady=5,  sticky='w')

    def apply_changes(self):
        print(self.value_input.get())
        self.plotter.set_joint_and_update(self.node_selection.get(), self.value_input.get().split(','))


if __name__ == '__main__':
    gui = GUI()
    gui.window.mainloop()