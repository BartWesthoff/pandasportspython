from typing import Set

class Joint:

    # Is likelihood een floating point?
    def __init__(self, x: float, y: float, z: float, likelihood: float, name: str) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.likelihood = likelihood
        self.name = name

    def ToJson(self) -> Set(str, float, float, float, float):
        return {self.name: {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "likelihood": self.likelihood
        }}
