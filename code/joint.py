import math

import numpy as np


class Joint:
    def __init__(self, **kwargs):
        # self.iterator = 0
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
        self.offset_offset = 0
        self.reference_parents = []
        self.reference_dh_parameters = []

    # def next(self):
    #     iterator = self.iterator
    #     self.iterator = self.iterator + 1
    #     if self.iterator == len(self.children):
    #         self.iterator = 0
    #     return self.children[iterator] #yield

    def __getitem__(self, title):
        """
        Definition des Zugriffsoperators. Rekursive Suche des Joints mit angegebenem Titel.
        Liefert Knoten mit angegebenem Titel aus dem Unterbaum.
        :return: Jointobjekt
        """
        if self.title == title:
            return self
        if not len(self.children):
            return None
        for child in self.children:
            res = child[title]
            if res is not None:
                return res

    def append(self, joint):
        # setzt Elter als Elter für Kind
        joint.previous = self
        # Setzt Kind als Kind von Elter (Eintragen von Objekt in Liste Children)
        self.children.append(joint)
        self.transformationmatrices_to_children.append(None)

    def __repr__(self):
        return f"Title: {self.title}, Children: {self.children}"

    def generate_dh_matrices_to_children(self):
        """
        Berechnet die Transformationsmatrizen eines Knoten zu seinen Kindern und trägt sie in eine Liste ein.
        :return:
        """
        if not self.children:
            return
        for index, child in enumerate(self.children):
            # Wenn kein Referenzkind mit angegebenem Titel besteht:
            if not self.has_reference_child(child.title):
                # DH-Transformationsmatrix
                self.transformationmatrices_to_children[index] = \
                    np.array([[np.cos(child.angle + child.angle_offset),
                               -np.sin(child.angle + child.angle_offset) * np.cos(child.twist),
                               np.sin(child.angle + child.angle_offset) * np.sin(child.twist),
                               (child.length ) * np.cos(child.angle + child.angle_offset)],
                              [np.sin(child.angle + child.angle_offset),
                               np.cos(child.angle + child.angle_offset) * np.cos(child.twist),
                               -np.cos(child.angle + child.angle_offset) * np.sin(child.twist),
                               (child.length ) * np.sin(child.angle + child.angle_offset)],
                              [0, np.sin(child.twist), np.cos(child.twist), child.offset + child.offset_offset],
                              [0, 0, 0, 1]])
                child.generate_dh_matrices_to_children()
            else:
                child_reference_dh = child.get_reference_dh_for_parent(self.title)
                self.transformationmatrices_to_children[index] = np.array([[np.cos(
                    child_reference_dh["angle"] + child_reference_dh["angle_offset"]), -np.sin(
                    child_reference_dh["angle"] + child_reference_dh["angle_offset"]) * np.cos(
                    child_reference_dh["twist"]), np.sin(
                    child_reference_dh["angle"] + child_reference_dh["angle_offset"]) * np.sin(
                    child_reference_dh["twist"]), (child_reference_dh["length"] + child_reference_dh[
                    "offset_offset"]) * np.cos(child_reference_dh["angle"] + child_reference_dh["angle_offset"])],
                                                                           [np.sin(child_reference_dh["angle"] +
                                                                                   child_reference_dh["angle_offset"]),
                                                                            np.cos(child_reference_dh["angle"] +
                                                                                   child_reference_dh[
                                                                                       "angle_offset"]) * np.cos(
                                                                                child_reference_dh["twist"]), -np.cos(
                                                                               child_reference_dh["angle"] +
                                                                               child_reference_dh[
                                                                                   "angle_offset"]) * np.sin(
                                                                               child_reference_dh["twist"]), (
                                                                                        child_reference_dh["length"] +
                                                                                        child_reference_dh[
                                                                                            "offset_offset"]) * np.sin(
                                                                               child_reference_dh["angle"] +
                                                                               child_reference_dh["angle_offset"])],
                                                                           [0, np.sin(child_reference_dh["twist"]),
                                                                            np.cos(child_reference_dh["twist"]),
                                                                            child_reference_dh["offset"]],
                                                                           [0, 0, 0, 1]])

    def get_reference_dh_for_parent(self, title):
        """
        Gibt DH-Parameter zu einem Referenzelternknoten zurück.
        """
        for parent, dh in zip(self.reference_parents, self.reference_dh_parameters):
            if parent.title == title:
                return dh
        return None

    def generate_dh_matrix_to(self, title):
        '''
        Sucht angegebenes Objekt mit dem angegebenem Titel.
        Erzeugt Transformationsmatrix bis zu diesem Objekt.
        :param title: Titel von Zielobjekt
        :return: Transformationsmatrix von Objekt zu Zielobjekt
        '''
        if not self.children:
            return None
        for index, child in enumerate(self.children):
            if child.title == title:
                return self.transformationmatrices_to_children[index]
            res = child.generate_dh_matrix_to(title)
            if res is not None:
                return np.dot(self.transformationmatrices_to_children[index], res)
        return None

    def set_joint(self, *args):
        if type(args[0][0]) == list:
            args = ([float(v) for v in args[0][0]],)
        if self.type == "rotation":
            for child in self.children:
                child.angle_offset += math.radians(args[0][0])
        elif self.type == "translation":
            for child in self.children:
                child.offset_offset += args[0][0]
        # if self.previous is not None:
        self.generate_dh_matrices_to_children()
        self.previous.generate_dh_matrices_to_children()
        # for index, arg in enumerate(args[0][1:]):
        #     if self.reference_dh_parameters:
        #         if self.reference_dh_parameters[index]["type"] == "rotation":
        #             self.reference_dh_parameters[index]["angle_offset"] += float(arg)
        #         elif self.reference_dh_parameters[index]["type"] == "translation":
        #             self.reference_dh_parameters[index]["offset_offset"] += float(arg)
        #         self.reference_parents[index].generate_dh_matrices_to_children()
        #     else:
        #         break

    def set_joint_to_absolute(self, *args):
        if self.type == "rotation":
            self.angle_offset = args[0][0]
        elif self.type == "translation":
            self.offset_offset = args[0][0]
        self.previous.generate_dh_matrices_to_children()
        for index, arg in enumerate(args[0][1:]):
            if self.reference_dh_parameters:
                if self.reference_dh_parameters[index]["type"] == "rotation":
                    self.reference_dh_parameters[index]["angle_offset"] = float(arg)
                elif self.reference_dh_parameters[index]["type"] == "translation":
                    self.reference_dh_parameters[index]["offset_offset"] = float(arg)
                self.reference_parents[index].generate_dh_matrices_to_children()
            else:
                break

    def reset_joint_offsets(self):
        self.angle_offset = 0
        self.offset_offset = 0
        for dh in self.reference_dh_parameters:
            dh["angle_offset"] = 0
            dh["offset_offset"] = 0
        for parent in self.reference_parents:
            parent.generate_dh_matrices_to_children()
        self.previous.generate_dh_matrices_to_children()

    def has_reference_child(self, title):
        for child in self.children:
            if child.title == title:
                return child.previous.title != self.title
        return True
