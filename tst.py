import numpy

acdb = list[list[int, float, numpy.ndarray]]()

acdb.append(())
acdb[0][0] = 2
acdb[0][1] = 2.5
acdb[0][2] = numpy.array([1, 2, 3])

print(acdb[0][0])