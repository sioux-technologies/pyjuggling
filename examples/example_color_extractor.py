import cv2

from juggling.circle_detector import CircleDetector
from juggling.color_extractor import ColorExtractor


image = cv2.imread("../tests/samples/circles_simple_red_amount_3.png")
circle_positions = CircleDetector(image).get(3)
for position in circle_positions:
    ColorExtractor(image, position).extract()
