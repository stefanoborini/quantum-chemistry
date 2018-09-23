import numpy
import math
import distance

def angle(v1, v2, origin=None):
    v1_arr = numpy.array(v1)
    v2_arr = numpy.array(v2)
    if origin is None:
        origin = [0.0, 0.0, 0.0]
    origin_arr = numpy.array(origin)

    return math.atan2( 
        distance.norm(numpy.cross(normalize(v2_arr-origin_arr), normalize(v1_arr-origin_arr))),
        numpy.dot(normalize(v2_arr-origin_arr), normalize(v1_arr-origin_arr))
    ) 


def normalize(v):
    return v/distance.norm(v)
   
