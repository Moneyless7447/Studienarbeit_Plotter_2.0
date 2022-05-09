import math

import numpy as np

'''
Verwaltende Klasse für ein Gelenk (Joint). Mehrere Joints werden von einem Robotobjekt (Roboter) verwaltet. 
Enthält die Informationen der DH Parameter für dieses eine Gelenk und kennt (Referenz-)Elter und Kindjointobjekte 
bzw. erzeugt die Transformationsmatrizen zu den Kindern.

Managing class for a joint. Several joints are managed by one robot object (robot). 
Contains the information of the DH parameters for this one joint and knows (reference) parent and child joint objects. 
or generates the transformation matrices for the children.
'''
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



    def __getitem__(self, title):
        """
        Definition des Zugriffsoperators. Rekursive Suche des Joints mit angegebenem Titel.
        Liefert Knoten mit angegebenem Titel aus dem Unterbaum.
        :return: Jointobjekt

        Definition of the access operator. Recursive search of the join with specified title.
        Returns nodes with specified title from the subtree.
        :return: Jointobject
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

        Calculates the transformation matrices of a node to its children and enters them in a list.
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

        Returns DH parameters to a reference parent node.
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

        Searches for the specified object with the specified title.
        Generates transformation matrix up to this object.
        :param title: Title of target
        :return: Transformation matrix from object to target object
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
        '''
        Setzt die zugehörigen Offsetparameter bei einer Veränderung (Rotation/Verschiebung) durch z.B. die Nutzung der GUI
        und berechnet die Transformationsmatrizen der Elter zu sich selbst neu.

        Sets the associated offset parameters in case of a change (rotation/shift) through e.g. the use of the GUI.
        and recalculates the transformation matrices of the parents to itself.

        '''
        if type(args[0][0]) == list:
            args = ([float(v) for v in args[0][0]],)
        if self.type == "rotation":
            for child in self.children:
                child.angle_offset += math.radians(args[0][0])
        elif self.type == "translation":
            for child in self.children:
                child.offset_offset += args[0][0]
        self.generate_dh_matrices_to_children()
        self.previous.generate_dh_matrices_to_children()


    def set_joint_to_absolute(self, *args):
        '''
        Setzt neue DH Paramter für dieses Gelenk (Joint) und
        berechnet die Transformationsmatrix von dem Elter zu sich selbst neu.


        Sets new DH parameters for this joint and
        recalculates the transformation matrix from the parent to itself.

        '''
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

    def set_angle_offset(self, value):
        self.angle_offset = value

    def reset_joint_offsets(self, *args):
        '''
        Setzt die Offsetwerte (durch Veränderungen) dieses Gelenks (Joints) zurück und
        berechnet die Transformationsmatrix von dem zugehöreigen Elter zu sich selbst neu.

        Resets the offset values (by changes) of this joint (Joints) and
        recalculates the transformation matrix from the associated parent to itself.

        '''
        self.set_angle_offset(0)
        self.offset_offset = 0
        for dh in self.reference_dh_parameters:
            dh["angle_offset"] = 0
            dh["offset_offset"] = 0
        for parent in self.reference_parents:
            parent.generate_dh_matrices_to_children()
        self.previous.generate_dh_matrices_to_children()

    def has_reference_child(self, title):
        '''
        Untersucht, ob dieses Gelenk (Joint) ein Referenzelter des gegebenen Kindes (title) ist.

        Investigates whether this joint is a reference parent of the given child (title).
        '''
        for child in self.children:
            if child.title == title:
                return child.previous.title != self.title
        return True

    def get_joint_offsets(self):
        return [self.angle_offset, self.offset_offset]

    # def next(self):
    #     iterator = self.iterator
    #     self.iterator = self.iterator + 1
    #     if self.iterator == len(self.children):
    #         self.iterator = 0
    #     return self.children[iterator] #yield