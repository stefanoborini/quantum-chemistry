import types
import numpy

class Measure:
    def __init__(self, value, unit): # fold>>
        self._value = value
        self._unit = unit

# <<fold
    def value(self): # fold>>
        return self._value
        # <<fold
    def unit(self): # fold>>
        return self._unit
        # <<fold
    def asUnit(self, new_unit): # fold>>
        if type(self._value) == types.TupleType or type(self._value) == types.ListType or type(self._value) == numpy.ndarray:
            new_value=[]
            for val in self._value:
                converted = (val*self._unit).asUnit(new_unit).asNumber()
                new_value.append(converted)
      
            if type(self._value) == types.TupleType:
                new_value = tuple(new_value)
            elif type(self._value) == numpy.ndarray:
                new_value = numpy.array(new_value)
        else:
            new_value = (self._value*self._unit).asUnit(new_unit).asNumber()
            
        return Measure(new_value, new_unit)
        # <<fold
    def __str__(self): # fold>>
        return str(self._value) + " " + self._unit.strUnit()
        # <<fold
    def __neg__(self): # fold>>
        if type(self._value) == types.TupleType or type(self._value) == types.ListType or type(self._value) == numpy.ndarray:
            new_value=[]
            for val in self._value:
                new_value.append(-val)
      
            if type(self._value) == types.TupleType:
                new_value = tuple(new_value)
            elif type(self._value) == numpy.ndarray:
                new_value = numpy.array(new_value)
        else:
            new_value = -self._value
            
        return Measure(new_value, self._unit)
        # <<fold
    def __add__(self, other): # fold>>
        self_is_list_type = (type(self._value) == types.TupleType or type(self._value) == types.ListType or type(self._value) == numpy.ndarray)
        other_is_list_type = (type(other._value) == types.TupleType or type(other._value) == types.ListType or type(other._value) == numpy.ndarray)
        
        if self_is_list_type and other_is_list_type:
            new_values = []
            for value_self, value_other in zip(self.value(), other.value()):
                new_value = value_self*self.unit() + value_other * other.unit()
                new_values.append(new_value.asUnit(self.unit()).asNumber())
            return Measure(new_values, self.unit())
        elif self_is_list_type and not other_is_list_type:
            new_values = []
            for value_self in self.value():
                new_value = value_self*self.unit() + other.value() * other.unit()
                new_values.append(new_value.asUnit(self.unit()).asNumber())
            return Measure(new_values, self.unit())
        elif not self_is_list_type and other_is_list_type:
            new_values = []
            for value_other in other.value():
                new_value = self.value() * self.unit() + value_other*other.unit()
                new_values.append(new_value.asUnit(self.unit()).asNumber())
            return Measure(new_values, self.unit())
        else:
            new_value = self.value()*self.unit() + other.value() * other.unit()
            return Measure(new_value.asUnit(self.unit()).asNumber(), self.unit())
        # <<fold 
    def __sub__(self, other): # fold>>
        self_is_list_type = (type(self._value) == types.TupleType or type(self._value) == types.ListType or type(self._value) == numpy.ndarray)
        other_is_list_type = (type(other._value) == types.TupleType or type(other._value) == types.ListType or type(other._value) == numpy.ndarray)

        if self_is_list_type and other_is_list_type:
            new_values = []
            for value_self, value_other in zip(self.value(), other.value()):
                new_value = value_self*self.unit() - value_other * other.unit()
                new_values.append(new_value.asUnit(self.unit()).asNumber())
            return Measure(new_values, self.unit())
        elif self_is_list_type and not other_is_list_type:
            new_values = []
            for value_self in self.value():
                new_value = value_self*self.unit() - other.value() * other.unit()
                new_values.append(new_value.asUnit(self.unit()).asNumber())
            return Measure(new_values, self.unit())
        elif not self_is_list_type and other_is_list_type:
            new_values = []
            for value_other in other.value():
                new_value = self.value() * self.unit() - value_other*other.unit()
                new_values.append(new_value.asUnit(self.unit()).asNumber())
            return Measure(new_values, self.unit())
        else:
            new_value = self.value()*self.unit() - other.value() * other.unit()
            return Measure(new_value.asUnit(self.unit()).asNumber(), self.unit())
        # <<fold 
