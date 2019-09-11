import numpy


class Matcher:
    def __init__(self, feature):
        self.__feature = feature

    def __similarity(self, other_feature):
        return numpy.sum(
            numpy.square(numpy.array(self.__feature) - numpy.array(other_feature)))  # Euclidean Square distance

    def match(self, features):
        if len(features) == 1:
            return self.__similarity(features[0]), features[0]

        index, distance = 0, self.__similarity(features[0])
        for i in range(1, len(features)):
            candidate_distance = self.__similarity(features[i])
            if self.__similarity(features[i]) < distance:
                index = i
                distance = candidate_distance

        return distance, features[index]
