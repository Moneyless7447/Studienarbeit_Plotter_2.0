import numpy as np
import json
from joint import Joint
import os

'''
Konvertiert eine gegebene Baumstruktur (JSON Format) in eine Objektbaumstruktur (Robot)
mit Doppelverlinkungen (nutzt die Klasse Joints). 

Converts a given tree structure (JSON format) into an object tree structure (Robot).
with double links (uses the Joints class). 
'''

class Robot:

    def __init__(self, robot_name, file_name):
        self.name = robot_name
        # setze Dummygelenk als Ursprung/Basis, sollte so gesetzt bleiben
        self.root = Joint(name="0", angle=0, length=0, offset=0, twist=0, title="root",
                          type=None, children=[], previous=None)
        self.build_from_json(file_name)
        self.root.generate_dh_matrices_to_children()

    def build_from_json(self, file_name: str):
        '''
        Rekursives Durchlaufen der Baumstruktur (JSON Datei) um verkettete Objekte zu erzeugen
        :param file_name: Name der JSON Roboter Datei, wird in "main.py" gesetzt und kann dort angepasst werden

        Recursive traversal of the tree structure (JSON file) to create concatenated objects.
        :param file_name: Name of the JSON robot file, is set in "main.py" and can be adjusted there.
        '''
        # laden der Daten
        # Load the data
        with open(os.path.join(".", file_name)) as data:
            test_data = json.load(data)
            # Ausgabe der erhaltenen Daten in der Konsole
            # Output of the received data in the console

            print(f"test_data from json: {test_data}")
        self.append_children(self.root, test_data["robot"])

    def append_children(self, parent, children_list):
        '''
        Erzeugt Instanzen von Joint. Verkettet diese objekte miteinander als doppelte Verkettung,
        ein Objekt hat ein Elter und kann mehrere Kinder haben.
        :param parent: Elter Objekt

        Creates instances of Joint. Concatenates these objects with each other as a double concatenation,
        an object has a parent and can have multiple children.
        :param parent: Parent object
        '''
        # Abbruchkriterium (Das Jointobjekt hat keine Kinder)
        # Termination criterion (The joint object has no children)
        if not children_list:
            return

        # Iteratives durchlaufen der Kinder
        # Iterative cycling through the children
        for index, child in enumerate(children_list):
            # str:"pi" in json zu float:np.pi umwandeln
            # <editor-fold desc="str:"pi" in json zu float:np.pi umwandeln">
            # Möglichkeiten: 2*pi  pi/6 pi und andere Vorzeichen
            #### ANGLE ####
            tmp_angle = child['angle']
            is_angle_pi = False
            is_angle_div = False
            #Prüfen, ob "pi" im String vorkommt
            # Check whether "pi" occurs in the string
            for i in range(len(child['angle'])):
                if (child['angle'][i] == "p") and (child['angle'][i + 1] is not None and "i"):
                    is_angle_pi = True
                elif child['angle'][i] == "/":
                    is_angle_div = True

            if is_angle_pi == True:
                if is_angle_div == True:
                    if child['angle'][0] == "-":
                        tmp_float = float(child['angle'][4:])
                        tmp_angle = float(-(np.pi / tmp_float))
                    else:
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
            # Check whether "pi" occurs in the string
            for i in range(len(child['twist'])):
                if (child['twist'][i] == "p") and (child['twist'][i + 1] is not None and "i"):
                    is_twist_pi = True
                elif child['twist'][i] == "/":
                    is_twist_div = True

            if is_twist_pi == True:
                if is_twist_div == True:
                    if child['twist'][0] == "-":
                        tmp_float = float(child['twist'][4:])
                        tmp_twist = float(-(np.pi / tmp_float))
                    else:
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
            """Benennung der Joints"""
            # Hilfsvariable für Benennung der Joints
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

            """"""
            # Suche nach Duplikaten
            # Search for duplicates
            reference_child = self.root[child["title"]]
            # Wenn das Kind noch nicht existiert:
            if reference_child is None:
                # Joint Objekt wird erzeugt
                child_object = Joint(name=c_name, angle=tmp_angle, length=child["length"], offset=child["offset"],
                                  twist=tmp_twist, title=child["title"],
                                  type=child["type"], children=list(), previous=None)

                # Neues Kind an Elternknoten anhängen
                # Doppelte Verlinkung: Neues Kind wird als Kind von Elter gesetzt und Elter wird als Elter von neuem Kind gesetzt
                # Attach new child to parent node
                # Double linking: New child is set as child of parent and parent is set as parent of new child
                parent.append(child_object)
                # Wenn Kindknoten vorhanden:
                # If child node present:
                if "children" in child:
                    # Rekursives Anhängen der Kindknoten
                    self.append_children(child_object, child["children"])

            # Kind existiert schon -> Duplikat:
            # Child already exists -> duplicate:
            else:
                # Aktueller Knoten wird als Referenzelter des Kindes eingetragen
                # Current node is entered as the child's reference parent
                reference_child.reference_parents.append(parent)
                reference_child.reference_dh_parameters.append({"angle": float(tmp_angle), "length": float(child["length"]),
                                                                "offset": float(child["offset"]), "twist": float(tmp_twist), "type": child["type"], "angle_offset": 0.0, "offset_offset": 0.0})
                # Existierendes Kind wird an den aktuellen Knoten als Kind angehängt
                # Existing child is attached to the current node as a child
                parent.children.append(reference_child)
                parent.transformationmatrices_to_children.append(None)


    def generate_dh_matrix_from_to(self, _from, _to):
        '''
        Erzeugt DH Transformationsmatrix von Objekt A zu Objekt B.
        Voraussetzung: Objekt B ist Kind bzw. Nachkomme von Objekt A.
        :param _from: Titel von Objekt A
        :param _to: Titel von objekt B
        :return: Transformationsmatirx_A_B

        Generates DH transformation matrix from object A to object B.
        Prerequisite: Object B is a child or descendant of object A.
        :param _from: Title of object A
        :param _to: Title of object B
        :return: Transformationmatrix_A_B
        '''
        # Zugriff auf __getitem__
        # Access to __getitem__
        return self.root[_from].generate_dh_matrix_to(_to)

    def calc_inverse_dh_matrix(self, trans_matrix):
        #Rotationsanteil
        rotation_matrix = np.transpose(trans_matrix[:3, :3])
        #Translationsanteil
        translation_matrix = trans_matrix[:3, -1:]
        translation_matrix = np.dot(-rotation_matrix, translation_matrix)
        inverse_matrix = np.eye(4)
        inverse_matrix[0:3, 0:3] = rotation_matrix[0:3]
        inverse_matrix[0:3, 3] = translation_matrix[0:3, 0]
        #print(f"rotation_matrix:\n{rotation_matrix}")
        #print(f"translation_matrix:\n{translation_matrix}")
        #print(f"Inverse Matrix:\n{inverse_matrix}")
        return inverse_matrix

    # Funktion zum Aufrufen der set_joint Funktion für eines benannten Jointobjektes.
    # Function to call the set_joint function for a named joint object.
    def set_joint(self, title, *args):
        # print(title, args)
        self.root[title].set_joint(args)

    # Funktion zum Aufrufen der set_joint_to_absolute Funktion eines benannten Jointobjektes.
    # Function to call the set_joint_to_absolute function of a named joint object.
    def set_joint_to_absolute(self, title, value):
        self.root[title].set_joint_to_absolute(value)

    # Funktion zum Aufrufen der reset_joint_offsets Funktion für Kinder eines benannten Jointobjektes.
    # Function to call the reset_joint_offsets function for children of a named joint object.
    def reset_joint_offsets(self, title, *args):
        #if self.root[title].children is not None:
        if hasattr(self.root[title],"children"):
            for child in range(len(self.root[title].children)):
                self.root[title].children[child].reset_joint_offsets()
        return


    def get_joint_titles(self, joint=None):
        '''
        Gibt eine Liste mit den "Titles" aller Gelenke (Joints) dieses Roboters (Robot) zurück.

        Returns a list with the "Titles" of all joints of this robot.
        '''
        if joint is None:
            joint = self.root
        titles_list = [joint.title]
        for child in joint.children:
            if not joint.has_reference_child(child.title):
                titles_list += self.get_joint_titles(child)
        return titles_list

    def get_joint_offsets(self, title):
        return self.root[title].get_joint_offsets()