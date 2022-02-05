from dataclasses import dataclass

@dataclass
class Joint:

    name: str
    angle: float
    length: float
    offset: float
    twist: float
    title: str
    type: str
    children: list
    previous: str



