import cv2
import imutils
import numpy

stream = cv2.VideoCapture("ball_6.mp4")

prev_frame = None
cur_frame = None

while(True):
    color_ranges = [[(0, 170, 100), (10, 255, 255)], [(170, 170, 100), (180, 255, 255)]]
    _, frame = stream.read()
    if frame is None:
        print("Nothing to process.")
        exit(-1)

    # image = cv2.blur(frame, (21, 21))
    # image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # mask_color_hsv = cv2.inRange(image_hsv, color_ranges[0][0], color_ranges[0][1])
    # for index_range in range(1, len(color_ranges)):
    #     color_range = color_ranges[index_range]
    #     mask_additional_hsv = cv2.inRange(image_hsv, color_range[0], color_range[1])
    #     mask_color_hsv = cv2.bitwise_or(mask_color_hsv, mask_additional_hsv)
    # image_cropped = cv2.bitwise_and(image, image, mask=mask_color_hsv)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray, (21, 21))

    prev_frame = cur_frame
    cur_frame = gray

    if prev_frame is None:
        continue

    frame_delta = cv2.absdiff(prev_frame, cur_frame)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    mask = numpy.full((frame.shape[0], frame.shape[1]), 0, dtype=numpy.uint8)
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < 30:
            continue

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)

    frame = cv2.bitwise_or(frame, frame, mask=mask)
    cv2.imshow("Result", frame)
    cv2.waitKey(60)
