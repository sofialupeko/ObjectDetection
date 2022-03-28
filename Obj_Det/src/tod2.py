###
### tod2.py
### ObjectDetection
###
### Created by Sofia Lupeko
###

import time
import cv2
from imutils.video import FileVideoStream
from imutils.video import FPS
from sort import Sort
from needs import load_detections_csv, extract_boxes_and_conf, prepare_detects, show_cropped_frame


def search_in_trackers(trackers, frame, main_index, fps, original_fps) -> tuple[bool, int] | tuple[bool, None]:
    (h, w) = frame.shape[:2]
    for t in trackers:
        width_center = w / 2
        height_center = h / 2

        if main_index is None:
            if t[0] < width_center < t[2] and t[1] < height_center < t[3]:
                main_index = int(t[4])
                show_cropped_frame(frame, t, h, w, original_fps)
                fps.update()

                return True, main_index
        elif main_index == int(t[4]):
            show_cropped_frame(frame, t, h, w, original_fps)
            fps.update()

            return True, main_index

    return False, None


def crop_main_car():
    video_path = input("Enter video name: ")
    print("[INFO] loading video...")

    fvs = FileVideoStream(video_path).start()
    original_fps = fvs.stream.get(cv2.CAP_PROP_FPS)
    time.sleep(2.0)
    fps = FPS().start()

    tracker = Sort()

    detections_list = load_detections_csv(video_path)
    num_of_line = 0

    num_of_frame = 0

    # define the main car
    main_index = None

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
                found, main_index = search_in_trackers(trackers, frame, main_index, fps, original_fps)
                if not found:
                    main_index = None

    fps.stop()
    print(f"[INFO] elapsed time: {fps.elapsed():.2f}")
    print(f"[INFO] approx. FPS: {fps.fps():.2f}")

    cv2.destroyAllWindows()
    fvs.stop()


if __name__ == "__main__":
    crop_main_car()
