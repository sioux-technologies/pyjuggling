from juggling.metric import euclidean


class Matcher:
    def __init__(self, circle_feature):
        self.__circle_feature = circle_feature

    def match(self, circle_features, weight=None):
        index, distance = 0, euclidean(circle_features[0], weight)

        for i in range(1, len(circle_features)):
            candidate_distance = euclidean(self.__circle_feature, circle_features[i], weight)
            if candidate_distance < distance:
                index = i
                distance = candidate_distance

        return distance, circle_features[index]
