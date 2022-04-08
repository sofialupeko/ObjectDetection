###
### tod3.py
### ObjectDetection
###
### Created by Sofia Lupeko
###

import time
import cv2
import numpy as np
from imutils.video import FileVideoStream
from imutils.video import FPS


def unique_frames():
    folder_path = "assets/"
    video_path = folder_path + input("Enter video name: ")
    print("[INFO] loading video...")

    fvs = FileVideoStream(video_path).start()
    time.sleep(2.0)
    fps = FPS().start()

    old_frame = None

    while fvs.more():
        frame = fvs.read()
        if isinstance(frame, type(None)):
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if old_frame is not None:
            diff_frame = cv2.absdiff(gray, old_frame)
            percentage = (np.count_nonzero(diff_frame) * 100) / diff_frame.size
            if percentage > 80:
                cv2.imshow("Different frame", frame)

        old_frame = gray

        key = cv2.waitKey(100)
        if key == ord("q"):
            break

        fps.update()

    fps.stop()
    print(f"[INFO] elapsed time: {fps.elapsed():.2f}")
    print(f"[INFO] approx. FPS: {fps.fps():.2f}")

    # cleanup
    cv2.destroyAllWindows()
    fvs.stop()


if __name__ == "__main__":
    unique_frames()
