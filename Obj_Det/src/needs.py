import random
import cv2
import pandas as pd
import imutils
import numpy as np
from logging import Logger
from mymath import sq_from_rect


def load_detections_csv(video_path: str):
    logger = Logger("Errors")
    file_path = video_path.replace("mkv", "csv")
    try:
        data = pd.read_csv(filepath_or_buffer=file_path)
        return data
    except Exception as err:
        logger.error(str(err))


def confidence_generator():
    return float(random.randrange(80, 100))


def extract_boxes_and_conf(frame, detections_list: pd.DataFrame, num_of_line: int, num_of_frame: int):

    def grab_current_frame_boxes():
        conf = confidence_generator()
        confidences.append(conf)

        box = detections_list.iloc[num_of_line, 1:] * np.array([w, h, w, h])
        startX, startY, endX, endY = box.astype("int")
        boxes.append([startX, startY, endX, endY])

    (h, w) = frame.shape[:2]

    boxes = []
    confidences = []

    while num_of_line < len(detections_list):
        current_frame = detections_list.iloc[num_of_line, 0]

        if current_frame == num_of_frame:
            grab_current_frame_boxes()

            num_of_line += 1
        else:
            num_of_frame += 1
            break

    return boxes, confidences, num_of_line, num_of_frame


def prepare_detects(boxes, confidences):
    detects = []
    if len(boxes) != 0:
        detects = np.zeros((len(boxes), 5))
        count = 0
        for i in range(len(boxes)):
            b = boxes[i]
            box = np.array([b[0], b[1], b[2], b[3], confidences[i]])
            detects[count, :] = box[:]
            count += 1

    return detects


def show_cropped_frame(frame, track, height: int, width: int, fps):
    cx0, cy0, cx1, cy1 = sq_from_rect(x0=track[0], y0=track[1], x1=track[2], y1=track[3], height=height, width=width)
    cropped = frame[cy0:cy1, cx0:cx1]
    resized = imutils.resize(cropped, 416, 416)

    cv2.imshow("Main car", resized)
    cv2.waitKey(int(1000/fps))
