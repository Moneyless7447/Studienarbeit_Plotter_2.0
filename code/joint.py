from dataclasses import dataclass
from pprint import pprint

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
        self.angle = kwargs["angle"]
        self.length = kwargs["length"]
        self.offset = kwargs["offset"]
        self.twist = kwargs["twist"]
        self.title = kwargs["title"]
        self.type = kwargs["type"]
        self.children = kwargs["children"]
        self.previous = kwargs["previous"]

    def next(self):
        iterator = self.iterator
        self.iterator = self.iterator + 1
        if self.iterator == len(self.children):
            self.iterator = 0
        return self.children[iterator]


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
