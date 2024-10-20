import numpy

acdb = list[list[int, float, numpy.ndarray]]()

ascoria = [3.5, 2.5]
arr2 = numpy.array([2.5 , 3.5])

acdb.append( (4, 0.5, numpy.array(ascoria)))

print( arr2 + acdb[0][2])