class Joint:

    def __init__(self, x, y, z, likelihood, name):
        self.x = x
        self.y = y
        self.z = z
        self.likelihood = likelihood
        self.name = name

    def ToJson(self):
        return {self.name: {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "likelihood": self.likelihood
        }}
