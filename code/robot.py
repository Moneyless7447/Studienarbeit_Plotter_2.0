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
Konvertiert eine gegebene Baumstruktur (JSON Format) in eine Objektbaumstruktur 
(nutzt die Klasse Joints)
'''



class Robot:

    def __init__(self, robot_name, file_name):
        self.name: str = robot_name
        #self.rootelements = []
        self.root = Joint(name="0", angle=0, length=0, offset=0, twist=0, title="root", type=None, children=[], previous=None)
        self.build_from_json(file_name)
        self.root.generate_dh_matrices_to_children()


    def build_from_json(self, file_name: str):
        '''
        Rekursives Durchlaufen der Baumstruktur um verkettete Objekte zu erzeugen
        :param file_name: Name der JSON Roboter Datei
        :return: Liste aus allein erstellten Jointobjekten mit jeweiligen Attributen
        '''
        # laden der Daten
        with open(os.path.join(".", file_name)) as data:
            test_data = json.load(data)
        self.append_children(self.root, test_data["robot"])


    def append_children(self,parent, children_list):
        if not children_list:
            return
        for index, child in enumerate(children_list):


            child_object = Joint(name=f"{parent.name}.{(index+1)}", angle=child["angle"], length=child["length"], offset=child["offset"],
                              twist=child["twist"], title=child["title"],
                              type=child["type"], children=list(), previous=None)
            if "children" in child:
                self.append_children(child_object, child["children"])
            parent.append(child_object)


    def generate_dh_matrix_from_to(self, _from, _to):
        return self.root[_from].generate_dh_matrix_to(_to)

    def set_joint(self, title, value):
        self.root[title].set_joint(value)



