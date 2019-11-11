import cv2
import imutils
import numpy


class MovementDetector:
    def __init__(self):
        self.__prev_frame = None
        self.__cur_frame = None

    def crop(self, frame, threshold):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.blur(gray, (21, 21))

        self.__prev_frame = self.__cur_frame
        self.__cur_frame = gray

        if self.__prev_frame is None:
            return None

        frame_delta = cv2.absdiff(self.__prev_frame, self.__cur_frame)
        thresh = cv2.threshold(frame_delta, threshold, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        mask = numpy.full((frame.shape[0], frame.shape[1]), 0, dtype=numpy.uint8)
        rectangles = []
        for c in cnts:
            if cv2.contourArea(c) < 30:
                continue

            (x, y, w, h) = cv2.boundingRect(c)
            rectangles.append((x, y, w, h))
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 255), -1)

        result = cv2.bitwise_or(frame, frame, mask=mask)
        #cv2.imshow("Movements", result)
        return result, rectangles
