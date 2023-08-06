"""
This module contains the camera class
"""
import typing


class Camera:
    """
    This is the camera object for moving around a scene
    """
    def __init__(self, x: float = 0, y: float = 0):
        """
        :param x:
        :param y:
        """
        self.x = x
        self.y = y

    def get_pos(self) -> typing.Tuple[float, float]:
        """
        Returns the coordinates of the camera
        """
        return self.x, self.y
