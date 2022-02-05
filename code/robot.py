from dataclasses import dataclass
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

"""
class Joint:
    def __init__(self, **kwargs):
        
"""


class Robot:

    def __init__(self, robot_name):
        self.name: str = robot_name
        self.rootelements = []
        self.treestructure = {}



    #     def init_robot(self, file_name: str):
    #         self.treestructure = self.restructure_json(file_name)
    #         print(f"bla bla: {self.treestructure}")
    #
    # init_robot("example_robot_dh.json")

    """
    # Einlesen der JSON Datenstruktur und Erstellung von doppelt verketteten Jointobjekten
    def restructure_json(self, filename: str):
        '''
        Rekursives Durchlaufen der Baumstruktur um verkettete Objekte zu erzeugen
        :param filename: Name der JSON Roboter Datei
        :return: Liste aus allein erstellten Jointobjekten mit jeweiligen Attributen
        '''
        # laden der Daten
        with open(os.path.join(".", filename)) as data:
            test_data = json.load(data)


        def build_tree(data_list: list):
            # rekursive Funktion
            def _build_tree(data: dict, result: list = list(), key: str = "1", previous_key: str = "0"):
                # wenn keine children angegeben sind, muss es sich um ein aeusseren Knoten/ Blatt handeln,
                # letzte Rekursionsstufe
                if 'children' not in data:
                    # Erzeugen des Joint Objektes
                    child = Joint(key, data["angle"], data["length"], data["offset"], data["twist"], data["title"],
                                  data["type"],
                                  list(), previous_key)
                    result.append(child)
                    # Eintragen der Rootelemente in rootelements (Liste)
                    if previous_key == "0":
                        self.rootelements.append(key)
                    return child
                else:
                    # Erzeugen des Joint Objektes
                    parent = Joint(key, data["angle"], data["length"], data["offset"], data["twist"], data["title"],
                                   data["type"],
                                   list(), previous_key)
                    # Eintragen der Rootelemente in rootelements (Liste)
                    if previous_key == "0":
                        self.rootelements.append(key)
                    # Rekursiver Funktionsaufruf für Kinder
                    for index, value in enumerate(data['children']):
                        new_key = f"{key}.{index + 1}"
                        child = _build_tree(data=value, result=result, key=new_key, previous_key=key)
                        parent.children.append(child.name if child is not None else "")
                    result.append(parent)
                    return

            result = list()
            # iteratives Aufrufen der rekursiven Funktion für jedes Kind der Wurzel
            for index, value in enumerate(data_list):
                _build_tree(data=value, result=result, key=f"{index + 1}")
            return result

        robot = test_data['robot']
        joints = build_tree(robot)
        return joints
    """

    def restructure_json(self, filename: str):
        '''
        Rekursives Durchlaufen der Baumstruktur um verkettete Objekte zu erzeugen
        :param filename: Name der JSON Roboter Datei
        :return: Liste aus allein erstellten Jointobjekten mit jeweiligen Attributen
        '''
        # laden der Daten
        with open(os.path.join(".", filename)) as data:
            test_data = json.load(data)

        def build_tree(data_list: list):
            # rekursive Funktion
            def _build_tree(data: dict, result: dict = dict(), key: str = "1", previous_key: str = "0"):
                # wenn keine children angegeben sind, muss es sich um ein aeusseren Knoten/ Blatt handeln,
                # letzte Rekursionsstufe
                if 'children' not in data:
                    # Erzeugen des Joint Objektes
                    child = Joint(key, data["angle"], data["length"], data["offset"], data["twist"], data["title"],
                                  data["type"],
                                  list(), previous_key)
                    result.update({key: child})
                    # Eintragen der Rootelemente in rootelements (Liste)
                    if previous_key == "0":
                        self.rootelements.append(key)
                    return child
                else:
                    # Erzeugen des Joint Objektes
                    parent = Joint(key, data["angle"], data["length"], data["offset"], data["twist"], data["title"],
                                   data["type"],
                                   list(), previous_key)
                    # Eintragen der Rootelemente in rootelements (Liste)
                    if previous_key == "0":
                        self.rootelements.append(key)
                    # Rekursiver Funktionsaufruf für Kinder
                    for index, value in enumerate(data['children']):
                        new_key = f"{key}.{index + 1}"
                        child = _build_tree(data=value, result=result, key=new_key, previous_key=key)
                        parent.children.append(child.name if child is not None else "")
                    result.update({key: parent})
                    return

            result = dict()
            # iteratives Aufrufen der rekursiven Funktion für jedes Kind der Wurzel
            for index, value in enumerate(data_list):
                _build_tree(data=value, result=result, key=f"{index + 1}")
            return result

        robot = test_data['robot']
        joints = build_tree(robot)
        return joints
    # Erzeugt für geg. Rootelement (z.B. Beinansatz) eine kinematische Kette aller Gelenke für diesen Teilbaum
    def init_kin_chain(self, key_leg):
        '''
        Eine Liste aus Listen für Gelenk 1 bis n mit der kinematischen Kette fuer das jeweilige Gelenk bis zum
        Basiskoordinatensystem (oberste Wurzel -> Körper)
        :param key_leg: key des Rootelements der zu untersuchenden Struktur (z.B. 1. Gelenk von Bein 1)
        :return: Bsp.: [['0', '1'], ['0', '1', '1.1'], ['0', '1', '1.2'], ['0', '1', '1.1', '1.1.1],
                        ['0', '1', '1.1', '1.1.2']]
        '''

        kin_chain_list = [[key_leg]]

        #for i in range(len(joint.))


        return kin_chain_list

    # def init_robot(self, file_name:str):
    #     self.treestructure = self.restructure_json(file_name)

