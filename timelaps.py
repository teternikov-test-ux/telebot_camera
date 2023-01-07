import cv2
import time
import os
from datetime import datetime




# from utils import CFEVideoConf, image_resize
# save_path = 'saved/time.mp4'
# frames_per_second = 24.0
# config = CFEVideoConf(cap, filepath=save_path, res='720p')

timelapse_dir = "D:\\timelaps\\"
if not os.path.exists(timelapse_dir):
    os.mkdir(timelapse_dir)
count = 1
while True:
    try:
        cap = cv2.VideoCapture('rtsp://192.168.0.100:554/user=admin&password=Teternikov@1988@&channel=1&stream'
                               '=0.sdp?')
        now = datetime.now().strftime('%m-%d  %H-%M-%S')
        filename = f"{timelapse_dir}/{now} foto {count}.jpg"
        _, _, files = next(os.walk(timelapse_dir))
        file_count = len(files)
        print(file_count)
        if file_count >= 200:
            print("количество больше 200")
            # files.sort(key=lambda x: os.path.getmtime(x))
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
