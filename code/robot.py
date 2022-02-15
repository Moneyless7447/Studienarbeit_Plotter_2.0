from dataclasses import dataclass
from urllib import robotparser

import matplotlib.pyplot as plt
import numpy as np
import math
import json
from joint import Joint
from mpl_toolkits.mplot3d import Axes3D
import os

'''
Konvertiert eine gegebene Baumstruktur (JSON Format) in eine Objektbaumstruktur (Robot)
(nutzt die Klasse Joints). 
'''



class Robot:

    def __init__(self, robot_name, file_name):
        self.name = robot_name
        #self.name: str = robot_name
        #setze Dummygelenk als Ursprung/Basis
        self.root = Joint(name="0", angle=0, length=0, offset=0, twist=0, title="root", type=None, children=[], previous=None)
        self.build_from_json(file_name)
        self.root.generate_dh_matrices_to_children()


    def build_from_json(self, file_name: str):
        '''
        Rekursives Durchlaufen der Baumstruktur um verkettete Objekte zu erzeugen
        :param file_name: Name der JSON Roboter Datei
        '''
        # laden der Daten
        with open(os.path.join(".", file_name)) as data:
            test_data = json.load(data)
            print(f"test_data from json: {test_data}")
        self.append_children(self.root, test_data["robot"])

    #def append_children(self, parent, children_list, fake_children_list):
    def append_children(self,parent, children_list):
        '''
        Erzeugt Instanzen von Joint. Und verkettet diese objekte miteinander
        :param parent: Elter Objekt
        '''
        if not children_list:
            return

        for index, child in enumerate(children_list):

            ############### str:"pi" in json zu float:np.pi umwandeln ###############
            # <editor-fold desc="str:"pi" in json zu float:np.pi umwandeln">
            # Möglichkeiten: 2*pi  pi/6 pi
            #### ANGLE ####
            tmp_angle = child['angle']
            is_angle_pi = False
            is_angle_div = False
            #Prüfen, ob "pi" im String vorkommt
            for i in range(len(child['angle'])):
                if (child['angle'][i] == "p") and (child['angle'][i + 1] is not None and "i"):
                    is_angle_pi = True
                elif child['angle'][i] == "/":
                    is_angle_div = True

            if is_angle_pi == True:
                if is_angle_div == True:
                    tmp_float = float(child['angle'][3:])
                    tmp_angle = float(np.pi / tmp_float)
                else:
                    if len(child['angle']) >= 4:
                        tmp_float = float(child['angle'][0:-3])
                        tmp_angle = float(np.pi * tmp_float)
                    elif len(child['angle']) == 2:
                        tmp_angle = np.pi

            #### TWIST ####
            tmp_twist = child['twist']
            is_twist_pi = False
            is_twist_div = False
            # Prüfen, ob "pi" im String vorkommt
            for i in range(len(child['twist'])):
                if (child['twist'][i] == "p") and (child['twist'][i + 1] is not None and "i"):
                    is_twist_pi = True
                elif child['twist'][i] == "/":
                    is_twist_div = True

            if is_twist_pi == True:
                if is_twist_div == True:
                    tmp_float = float(child['twist'][3:])
                    tmp_twist = float(np.pi / tmp_float)
                else:
                    if len(child['twist']) >= 4:
                        tmp_float = float(child['twist'][0:-3])
                        tmp_twist = float(np.pi * tmp_float)
                    elif len(child['twist']) == 2:
                        tmp_twist = np.pi
            #########################################################################
            # </editor-fold>

            parent_dh_depth = parent.name.split("_")[-1]


            if parent.title != "root":
                if len(children_list) == 1:
                    if "_" in parent.name:
                        c_name = parent.name.split('_')[0]+ f"_{int(parent_dh_depth) + 1}"
                    else:
                        c_name = f"{int(parent_dh_depth) + 1}"
                else:
                    if "_" in parent.name:
                        c_name = parent.name.split('_')[0] + f".{index}" + f"_{int(parent_dh_depth) + 1}"
                    else:
                        c_name = f"{index}" + f"_{int(parent_dh_depth) + 1}"
            else:
                if len(children_list) == 1:
                    c_name = "1"
                else:
                    c_name = f"{index}_"+"1"

            reference_child = self.root[child["title"]]
            if reference_child is None:
                # Joint Objekt wird erzeugt
                child_object = Joint(name=c_name, angle=tmp_angle, length=child["length"], offset=child["offset"],
                                  twist=tmp_twist, title=child["title"],
                                  type=child["type"], children=list(), previous=None)

                # rekursiver Aufruf der Funktion für Kinder
                parent.append(child_object)
                if "children" in child:
                    self.append_children(child_object, child["children"])
                # Doppelte Verlinkung: Neues Kind wird als Kind von Elter gesetzt und Elter wird als Elter von neuem Kind gesetzt
                # parent.append(child_object)
            else:
                reference_child.reference_parents.append(parent)
                reference_child.reference_dh_parameters.append({"angle": float(tmp_angle), "length": float(child["length"]),
                                                                "offset": float(child["offset"]), "twist": float(tmp_twist), "type": child["type"], "angle_offset": 0.0, "length_offset": 0.0})
                parent.children.append(reference_child)
                parent.transformationmatrices_to_children.append(None)


    def generate_dh_matrix_from_to(self, _from, _to):
        '''
        Erzeugt DH Transformationsmatrix von Objekt A zu Objekt B.
        Voraussetzung: Objekt B ist Kind bzw. Nachkomme von Objekt A.
        :param _from: Titel von Objekt A
        :param _to: Titel von objekt B
        :return: Transformationsmatirx_A_B
        '''
        # Zugriff auf __getitem__
        return self.root[_from].generate_dh_matrix_to(_to)

    def set_joint(self, title, value):
        self.root[title].set_joint(value)

    def set_joint_to_absolute(self, title, value):
        self.root[title].set_joint_to_absolute(value)

    def reset_joint_offsets(self, title):
        self.root[title].reset_joint_offsets()


