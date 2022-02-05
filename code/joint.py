from dataclasses import dataclass

@dataclass
class Joint:

    # def __init__(self):
    #
    #     self.name: str
    #     self.angle: float
    #     self.length: float
    #     self.offset: float
    #     self.twist: float
    #     self.title: str
    #     self.type: str
    #     self.children: list
    #     self.previous: str

    name: str
    angle: float
    length: float
    offset: float
    twist: float
    title: str
    type: str
    children: str
    previous: str

