import numpy


def euclidean_square(object1, object2, weight=None):
    weight = weight or numpy.ones(len(object2))
    return numpy.sum(numpy.square(numpy.array(object1) * weight - numpy.array(object2) * weight))


def euclidean(object1, object2, weight=None):
    weight = weight or numpy.ones(len(object2))
    return numpy.sqrt(numpy.sum(numpy.square(numpy.array(object1) * weight - numpy.array(object2) * weight)))
