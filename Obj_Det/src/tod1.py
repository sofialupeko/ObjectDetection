###
### tod1.py
### ObjectDetection
###
### Created by Sofia Lupeko
###

import time
import random
import cv2
from imutils.video import FileVideoStream
from imutils.video import FPS
from sort import Sort
from needs import load_detections_csv, extract_boxes_and_conf, prepare_detects


def customize_tracks(trackers, frame, color_list):
    for t in trackers:
        p1, p2 = (int(t[0]), int(t[1])), (int(t[2]), int(t[3]))
        color = color_list[int(t[4])]
        frame = cv2.rectangle(frame, p1, p2, color, 2)
        label = str(int(t[4]))
        y = int(t[1]) - 15 if int(t[1]) - 15 > 15 else int(t[1]) + 15
        cv2.putText(frame, label, (int(t[0]), y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

def color_generation():
    color_list = []
    for i in range(1000):
        color_list.append((int(random.randrange(255)), int(random.randrange(255)), int(random.randrange(255))))
    return color_list


def track_detections():
    folder_path = "assets/"
    video_path = folder_path + input("Enter video name: ")
    print("[INFO] loading video...")

    fvs = FileVideoStream(video_path).start()
    original_fps = fvs.stream.get(cv2.CAP_PROP_FPS)
    time.sleep(2.0)
    fps = FPS().start()

    tracker = Sort()

    detections_list = load_detections_csv(video_path)
    num_of_line = 0

    num_of_frame = 0

    color_list = color_generation()

    while fvs.more():
        frame = fvs.read()
        if isinstance(frame, type(None)):
            break

        boxes, confidences, num_of_line, num_of_frame = extract_boxes_and_conf(frame,
                                                                               detections_list,
                                                                               num_of_line,
                                                                               num_of_frame)

        detects = prepare_detects(boxes, confidences)

        if len(detects) != 0:
            trackers = tracker.update(detects)
            if len(trackers) != 0:
                customize_tracks(trackers, frame, color_list)
        cv2.imshow("Frame", frame)

        key = cv2.waitKey(int(1000/original_fps))
        if key == ord("q"):
            break

        fps.update()

    fps.stop()
    print(f"[INFO] elapsed time: {fps.elapsed():.2f}")
    print(f"[INFO] approx. FPS: {fps.fps():.2f}")

    cv2.destroyAllWindows()
    fvs.stop()


if __name__ == "__main__":
    track_detections()
