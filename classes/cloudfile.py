from collections.abc import Iterable




class CloudFile:
    """class to represent a file downloaded from the cloud"""

    def __init__(self, id: str, name: str, parents: str) -> None:
        self._id = id,
        self._name = name,
        self.parents = parents,

    @property
    def name(self):
        # if name is of type tuple return first element
        if isinstance(self._name, Iterable):
            return self._name[0]
        # if name is of type string return string
        elif isinstance(self._name, str):
            return self._name
        else:
            raise ValueError("name is not of type string or tuple")

    @property
    def id(self):
        # if id is of type tuple return first element
        if isinstance(self._id, Iterable):
            return self._id[0]
        # if name is of type string return string
        elif isinstance(self._id, str):
            return self._id
        else:
            raise ValueError("name is not of type string or tuple")
