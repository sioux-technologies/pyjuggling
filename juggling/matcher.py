import numpy


class Matcher:
    def __init__(self, feature):
        self.__feature = feature

    def __similarity(self, other_feature, weight):
        if weight is None:
            weight = numpy.ones(len(other_feature))

        return numpy.sum(
            numpy.square(numpy.array(self.__feature) * weight - numpy.array(other_feature) * weight))

    def match(self, features, weight=None):
        index, distance = 0, self.__similarity(features[0], weight)

        for i in range(1, len(features)):
            candidate_distance = self.__similarity(features[i], weight)
            if candidate_distance < distance:
                index = i
                distance = candidate_distance

        return distance, features[index]
