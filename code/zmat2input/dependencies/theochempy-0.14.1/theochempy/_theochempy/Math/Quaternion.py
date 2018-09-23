import _Gohlke_transformations
from theochempy._theochempy import Units


import math

class Quaternion:
    def __init__(self, axis, angle): # fold>>
        self._angle = angle
        self._axis = axis

        self._w_value = math.cos(angle.asUnit(Units.radians).value()/2.0)

        s = math.sin(angle.asUnit(Units.radians).value()/2.0)
        self._x_value = float(axis.value()[0])*s
        self._y_value = float(axis.value()[1])*s
        self._z_value = float(axis.value()[2])*s
        # <<fold
    def _w(self): # fold>>
        return self._w_value
        # <<fold
    def _x(self): # fold>>
        return self._x_value
        # <<fold
    def _y(self): # fold>>
        return self._y_value
        # <<fold
    def _z(self): # fold>>
        return self._z_value
        # <<fold
    def toRotationMatrix(self): # fold>>
        return _Gohlke_transformations.quaternion_matrix((self._x_value, self._y_value, self._z_value, self._w_value))
        # <<fold
        
