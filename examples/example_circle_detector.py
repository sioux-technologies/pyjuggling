import cv2

from juggling.circle_detector import CircleDetector


def example(image_path, amount):
    image = cv2.imread(image_path)
    circles = CircleDetector(image).get(amount)

    if circles is None:
        print("Required amount of circles is not detected.")
        return

    for circle in circles:
        cv2.circle(image, (int(circle[0]), int(circle[1])), int(circle[2]), (0, 255, 0), 2)
        cv2.circle(image, (int(circle[0]), int(circle[1])), 2, (0, 0, 255), 3)

    cv2.imshow('Juggling', image)
    cv2.waitKey(0)


example("../tests/samples/circles_simple_colored_amount_3.png", 3)
example("../tests/samples/circles_simple_colored_amount_3_noise.png", 3)
example("../tests/samples/circles_simple_red_amount_3.png", 3)
example("../tests/samples/circles_simple_red_amount_3_noise.png", 3)
example("../tests/samples/circles_simple_colored_amount_5.png", 5)
example("../tests/samples/circles_photo_amount_3_white_background_1.jpg", 3)
example("../tests/samples/circles_photo_amount_3_white_background_2.jpg", 3)
example("../tests/samples/circles_photo_colored_amount_6.png", 6)
