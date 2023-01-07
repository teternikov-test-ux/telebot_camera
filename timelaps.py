import cv2
import time
import os
from datetime import datetime
from config import timelapse_dir, videourl

if not os.path.exists(timelapse_dir):
    os.mkdir(timelapse_dir)
count = 1
while True:
    try:
        cap = cv2.VideoCapture(videourl)
        now = datetime.now().strftime('%m-%d  %H-%M-%S')
        filename = f"{timelapse_dir}/{now} foto {count}.jpg"
        _, _, files = next(os.walk(timelapse_dir))
        file_count = len(files)
        print(file_count)
        if file_count >= 100:
            print("количество больше 100")
            print(files[1])
            os.path.isfile(f"{timelapse_dir}/{files[1]}")
            os.remove(f"{timelapse_dir}/{files[1]}")
            print(file_count)
        else:
            print("делаю скриншот")
            ret, frame = cap.read()
            count += 1
            cv2.imwrite(filename, frame)
            time.sleep(300)
    except BaseException:
        print("что то пошло не так")
        raise
