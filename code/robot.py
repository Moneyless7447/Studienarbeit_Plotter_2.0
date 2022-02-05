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



class Robot:

    def __init__(self, robot_name):
        self.name: str = robot_name
        self.rootelements: list


    def restructure_json(self, filename: str):
        with open(os.path.join(".", filename)) as data:
            test_data = json.load(data)

        def build_tree(data_list: list):
            def _build_tree(data: dict, result: list = list(), key: str = "1", previous_key: str = "0"):
                if 'children' not in data:
                    child = Joint(key, data["angle"], data["length"], data["offset"], data["twist"], data["title"],
                                  data["type"],
                                  list(), previous_key)
                    result.append(child)

                    return child
                else:
                    parent = Joint(key, data["angle"], data["length"], data["offset"], data["twist"], data["title"],
                                   data["type"],
                                   list(), previous_key)

                    for index, value in enumerate(data['children']):
                        new_key = f"{key}.{index + 1}"
                        child = _build_tree(data=value, result=result, key=new_key, previous_key=key)
                        parent.children.append(child.name if child is not None else "")
                    result.append(parent)
                    return

            result = list()
            for index, value in enumerate(data_list):
                _build_tree(data=value, result=result, key=f"{index + 1}")
            return result

        robot = test_data['robot']
        joints = build_tree(robot)
        return joints

