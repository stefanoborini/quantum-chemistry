import numpy

def pointFromLine(line_first, line_second, point):
    line_first_arr = numpy.array(line_first)
    line_second_arr = numpy.array(line_second)
    point_arr = numpy.array(point)

    numerator = norm( numpy.cross( (line_second_arr - line_first_arr), (line_first_arr - point) ) )
    denominator = norm(line_second_arr - line_first_arr)
    return numerator / denominator

def orthogonalVector(line_first, line_second, point):
    line_first_arr = numpy.array(line_first)
    line_second_arr = numpy.array(line_second)
    point_arr = numpy.array(point)

    t = - (numpy.dot(line_first_arr - point_arr, line_second_arr - line_first_arr)) / norm( line_second_arr-line_first_arr)**2

    minimum = line_first_arr + ( line_second_arr-line_first_arr) * t
    return point_arr - minimum

def norm(vector):
    return numpy.sqrt(numpy.vdot(vector,vector))

