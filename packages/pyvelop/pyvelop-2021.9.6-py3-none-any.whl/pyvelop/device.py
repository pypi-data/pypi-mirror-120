"""Representation of a mesh device"""

from .base import MeshDevice


class Device(MeshDevice):
    """Represents a user device in the mesh, i.e. not a node"""

    def __init__(self, **kwargs):
        """Constructor

        :param kwargs: keyword arguments
        """
        self.__attributes = kwargs
        self.__device_id = self.__attributes.get("deviceID")
        super().__init__(**kwargs)
