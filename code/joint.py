from dataclasses import dataclass
from pprint import pprint
import numpy as np

#
# @dataclass
# class Joint:
#     name: str
#     angle: float
#     length: float
#     offset: float
#     twist: float
#     title: str
#     type: str
#     children: list
#     previous: str
#

class Joint:
    def __init__(self, **kwargs):
        self.iterator = 0
        self.name = kwargs["name"]
        self.angle = float(kwargs["angle"])
        self.length = float(kwargs["length"])
        self.offset = float(kwargs["offset"])
        self.twist = float(kwargs["twist"])
        self.title = kwargs["title"]
        self.type = kwargs["type"]
        self.children = kwargs["children"]
        self.previous = kwargs["previous"]
        self.transformationmatrices_to_children = []
        self.angle_offset = 0
        self.length_offset = 0

    # def next(self):
    #     iterator = self.iterator
    #     self.iterator = self.iterator + 1
    #     if self.iterator == len(self.children):
    #         self.iterator = 0
    #     return self.children[iterator] #yield

    def __getitem__(self, title):
        if self.title == title:
            return self
        if not len(self.children):
            return None
        for child in self.children:
            res = child[title]
            if res is not None:
                return res

    def append(self, joint):
        joint.previous = self
        self.children.append(joint)
        self.transformationmatrices_to_children.append(None)

    def __repr__(self):
        return f"Title: {self.title}, Children: {self.children}"

    def generate_dh_matrices_to_children(self):
        if not self.children:
            return
        for index, child in enumerate(self.children):

            self.transformationmatrices_to_children[index] = np.array([[np.cos(child.angle+child.angle_offset), -np.sin(child.angle+child.angle_offset)*np.cos(child.twist), np.sin(child.angle+child.angle_offset)*np.sin(child.twist), child.length*np.cos(child.angle+child.angle_offset)],
                                                                       [np.sin(child.angle+child.angle_offset), np.cos(child.angle+child.angle_offset)*np.cos(child.twist), -np.cos(child.angle+child.angle_offset)*np.sin(child.twist), (child.length+child.length_offset) * np.sin(child.angle+child.angle_offset)],
                                                                       [0, np.sin(child.twist), np.cos(child.twist), child.offset],
                                                                       [0, 0, 0, 1]])
            child.generate_dh_matrices_to_children()


    def generate_dh_matrix_to(self, title):
        if not self.children:
            return None
        for index, child in enumerate(self.children):
            if child.title == title:
                return self.transformationmatrices_to_children[index]
            res = child.generate_dh_matrix_to(title)
            if res is not None:
                return np.dot(self.transformationmatrices_to_children[index], res)
        return None


    def set_joint(self, value):
        if self.type == "rotation":
            self.angle_offset = value
        elif self.type == "translate":
            self.length_offset = value
        self.previous.generate_dh_matrices_to_children()



if __name__ == "__main__":
    branch_2_data = {"name": "name2",
                     "angle": "angle",
                     "length": "length",
                     "offset": "offset",
                     "twist": "twist",
                     "title": "title",
                     "type": "type",
                     "children": [],
                     "previous": "previous"}

    j2 = Joint(**branch_2_data)

    branch_1_data = {"name": "name1",
                     "angle": "angle",
                     "length": "length",
                     "offset": "offset",
                     "twist": "twist",
                     "title": "title",
                     "type": "type",
                     "children": [],
                     "previous": "previous"}

    j1 = Joint(**branch_1_data)

    root_data = {"name": "name",
                 "angle": "angle",
                 "length": "length",
                 "offset": "offset",
                 "twist": "twist",
                 "title": "title",
                 "type": "type",
                 "children": [j1, j2],
                 "previous": "previous"}

    j = Joint(**root_data)
    pprint(j.next().name)
    pprint(j.next().name)
    pprint(j.next().name)
    pprint(j.next().name)
    j1.name="neuer Name"
    pprint(j.next().name)
    pprint(j.next().name)
    pprint(j.next().name)
    pprint(j.next().name)
