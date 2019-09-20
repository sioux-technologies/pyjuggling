import cv2
from juggling.circle_detector import ColorCircleDetector


images = ["../tests/samples/circles_simple_red_amount_3_02.png",
          "../tests/samples/circles_simple_red_amount_3_01.png",
          "../tests/samples/photo_reddish_ball_01.jpg",
          "../tests/samples/photo_reddish_ball_02.jpg",
          "../tests/samples/photo_reddish_ball_03.jpg",
          "../tests/samples/photo_reddish_ball_04.jpg",
          "../tests/samples/photo_reddish_ball_05.jpg",
          "../tests/samples/photo_reddish_ball_06.jpg",
          "../tests/samples/photo_reddish_ball_07.jpg",
          "../tests/samples/photo_reddish_ball_08.jpg",
          "../tests/samples/photo_reddish_ball_09.jpg",
          "../tests/samples/photo_reddish_ball_10.jpg",
          "../tests/samples/photo_reddish_ball_11.jpg",
          "../tests/samples/photo_reddish_ball_12.jpg"]

count = [3, 3, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 2, 2]

# images = ["../tests/samples/photo_reddish_ball_12.jpg"]
# count = [2]

for i in range(len(images)):
    path = images[i]
    amount = count[i]

    image = cv2.imread(path)
    color_ranges = [[(0, 150, 120), (10, 255, 255)], [(170, 150, 120), (180, 255, 255)]]
    circles = ColorCircleDetector(image, color_ranges).get(amount)
    if circles is not None:
        for circle in circles:
            x, y, r = circle[0], circle[1], circle[2]
            cv2.rectangle(image, (x - r, y - r), (x + r, y + r), (0, 255, 0), thickness=2)

        cv2.imshow("Result", image)
        cv2.waitKey(0)

    else:
        print("Nothing is found for '%s'." % path)
        cv2.waitKey(0)
