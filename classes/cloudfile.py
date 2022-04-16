class CloudFile:

    def __init__(self, id, name, parents):
        self.id = id,
        self._name = name,
        self.parents = parents,


    @property
    def name(self):
        # if name is of type tuble return first element
        if isinstance(self._name, tuple):
            return self._name[0]
        # if name is of type string return string
        elif isinstance(self._name, str):
            return self._name
        else:
            raise ValueError("name is not of type string or tuple")

