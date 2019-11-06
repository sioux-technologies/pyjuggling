from juggling.metric import euclidean


class MatchResult:
    def __init__(self, index_circle, position, distance, relible):
        self.index_circle = index_circle
        self.next_position = position
        self.distance = distance
        self.relible = relible

    def __str__(self):
        return str("circle: '%d', distance: '%f', position '%s'" %
                   (self.index_circle, self.distance, str(self.next_position)))

    def __repr__(self):
        return str(self)


class Matcher:
    def __init__(self, image_height, image_width, circles):
        self.__height = image_height
        self.__width = image_width

        self.__circles = circles

        self.__max_x = self.__width
        self.__max_y = self.__height
        self.__max_color = [255, 255, 255]
        self.__max_radius = min(self.__height, self.__width) / 2

    def _normalize_features(self, positions):
        result = []
        for i in range(len(positions)):
            result.append(self._normalize_same_color_feature(positions[i]))

        return result

    def _normalize_feature(self, position):
        return self._normalize_same_color_feature(position)

    def _normalize_same_color_feature(self, position):
        return [position[0],    # x
                position[1],    # y
                0]              # v

    def match(self, next_positions):
        """
        Find the more likely position for each circle by calculating dissimilarity and position prediction in line
        with telemetry.

        :param next_positions: New positions for each circle.
        :return: Most probable position for each circle.
        :type: array_like
        """
        extracted_patterns = self._normalize_features(next_positions)
        circle_dissimilarity = []

        for i in range(len(self.__circles)):
            current_circle = self.__circles[i]
            current_pattern = [current_circle.get_position()[0], current_circle.get_position()[1],
                               current_circle.get_velocity()]

            for index_pattern in range(len(extracted_patterns)):
                vx_theoretical = extracted_patterns[index_pattern][0] - current_circle.get_position()[0]
                vy_theoretical = extracted_patterns[index_pattern][1] - current_circle.get_position()[1]
                v_theoretical = pow(pow(vx_theoretical, 2) + pow(vy_theoretical, 2), 0.5)

                extracted_patterns[index_pattern][2] = v_theoretical
                distance = euclidean(current_pattern, extracted_patterns[index_pattern])
                circle_dissimilarity.append((i, index_pattern, distance))

        circle_dissimilarity.sort(key=lambda descriptor: descriptor[2])
        assigned_patterns = set()
        updated_circles = set()

        result = []
        for item in circle_dissimilarity:
            index_circle = item[0]
            index_pattern = item[1]
            distance = item[2]

            if (index_pattern in assigned_patterns) or (index_circle in updated_circles):
                continue

            reliable = True
            x_change = next_positions[index_pattern][0] - self.__circles[index_circle].get_position()[0]
            y_change = next_positions[index_pattern][1] - self.__circles[index_circle].get_position()[1]
            velocity = pow(pow(x_change, 2) + pow(y_change, 2), 0.5)
            if velocity > self.__circles[index_circle].get_velocity() * 2:
                reliable = False

            # make sure that it is possible in line telemetry
            assigned_patterns.add(index_pattern)
            updated_circles.add(index_circle)

            result.append(MatchResult(index_circle, next_positions[index_pattern], distance, reliable))
            if len(result) == len(self.__circles):
                break

        return result
