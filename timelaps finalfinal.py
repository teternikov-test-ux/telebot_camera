import os
import cv2
import glob
import types
import telebot
from telebot import types
import time
from datetime import datetime


dt = str(datetime.now().strftime('%D %H:%M:%S'))
timelapse_dir = "D:\\timelaps\\"
if not os.path.exists(timelapse_dir):
    os.mkdir(timelapse_dir)
bot = telebot.TeleBot("5693489936:AAEBNeh5WrX49OwhUZBrd4RzEklfOES-JtY")
usernames = ['teternikov', 'inspire_4_me', 'SABarsuk']
ids = {1246216837, 315473369, 334879600}


@bot.message_handler(commands=["start"])
def start(m, res=False):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("фото")
        item2 = types.KeyboardButton("видео")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(m.chat.id, 'Нажми "фото" или "видео(таймлапс последних 200 фото)"', reply_markup=markup)
    except TypeError:
        raise


@bot.message_handler(content_types=['text'])
def photo(test):
    try:
        if test.text.strip() == 'фото' and test.from_user.username in usernames or test.text.strip() == 'фото' and test.from_user.id in ids:
            count = 1
            now = datetime.now().strftime('%m-%d  %H-%M-%S')
            filename = f"{timelapse_dir}/{now} foto {count}.jpg"
            bot.send_message(test.chat.id, " через несколько секунд будет фото ")
            vidcap = cv2.VideoCapture('rtsp://192.168.0.100:554/user=admin&password=Teternikov@1988@&channel=1&stream'
                                      '=0.sdp?')
            if not vidcap:
                print("!!! Failed VideoCapture: invalid parameter!")
            success, image = vidcap.read()
            if success:

                cv2.imwrite(filename, image)
                bot.send_photo(test.chat.id, photo=open(filename, 'rb'), caption=f"{dt} Фото отправлено")
                if test.from_user.username:
                    print(dt + " === сделано фото  " + test.from_user.username)
                else:
                    print(dt + " === сделано фото  " + str(test.from_user.id))
            else:
                print("не удалось картинку отправить")
        elif test.text.strip() == 'видео' and test.from_user.username in usernames or test.text.strip() == 'видео' and test.from_user.id in ids:
            bot.send_message(test.chat.id, " через несколько секунд будет видео ")
            # height = 1440
            # width = 2560
            height = 1080
            width = 1920

            video = cv2.VideoWriter(timelapse_dir + "video" + ".avi", cv2.VideoWriter_fourcc(*'DIVX'), 3,
                                    (width, height))

            filesforvideo = glob.glob(f"{glob.escape(timelapse_dir)}/*.jpg")
            filesforvideo.sort(key=os.path.getmtime)

            for screenshot in filesforvideo:
                origImage = cv2.imread(screenshot)
                heightOrig, widthOrig, channelsOrig = origImage.shape
                if height != heightOrig or width != widthOrig:
                    img = cv2.resize(origImage, (width, height))
                    video.write(img)
                else:
                    video.write(origImage)
            video.release()
            # time.sleep(5)
            # bot.send_message(test.chat.id, "видео готово")
            bot.send_video(test.chat.id, video=open(timelapse_dir + 'video.avi', 'rb'), caption=dt + 'получите видео')
            if test.from_user.username:
                print(dt + " === сделано видео  " + test.from_user.username)
            else:
                print(dt + " === сделано видео  " + str(test.from_user.id))
        else:
            bot.send_message(test.chat.id, "Что то пошло не так")
    except BaseException:
        raise


bot.infinity_polling(interval=0, timeout=600)


# def photo():
#     count = 1
#     cap = cv2.VideoCapture('rtsp://192.168.0.100:554/user=admin&password=Teternikov@1988@&channel=1&stream'
#                                    '=0.sdp?')
#     now = datetime.now().strftime('%m-%d  %H-%M-%S')
#     filename = f"{timelapse_dir}/{now} foto {count}.jpg"
#     print(now)
#     ret, frame = cap.read()
#     count += 1
#     cv2.imwrite(filename, frame)
#
#
# schedule.every(1).seconds.do(photo)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)



# def test(photo, self=None):
#     height = 1080
#     width = 1920
#
#     video = cv2.VideoWriter(dirToSave + photo + ".avi", cv2.VideoWriter_fourcc(*'DIVX'), 5, (width, height))
#
#     files = glob.glob(f"{glob.escape(dirToSave)}/*.jpg")
#     files.sort(key=os.path.getmtime)
#     # files = os.listdir(dirToSave)
#     # screenshots = list(filter(lambda x: x.endswith(".jpg"), files))
#
#     for screenshot in files:
#         origImage = cv2.imread(screenshot)
#         heightOrig, widthOrig, channelsOrig = origImage.shape
#         if height != heightOrig or width != widthOrig:
#             img = cv2.resize(origImage, (width, height))
#             video.write(img)
#         else:
#             video.write(origImage)
#     video.release()
#
# Очистка
#
#
# def cleanup(self, lapse_filename: str, force: bool = False) -> None:
#       lapse_dir = f"{self._base_dir}/{lapse_filename}"
#       if self._cleanup or force:
#           for filename in glob.glob(f"{glob.escape(lapse_dir)}/*.{self._img_extension}"):
#               os.remove(filename)
#           for filename in glob.glob(f"{glob.escape(lapse_dir)}/*"):
#               os.remove(filename)
#           Path(lapse_dir).rmdir()
#
# def clean(self) -> None:
#     if self._cleanup and self._klippy.printing_filename and os.path.isdir(self.lapse_dir):
#         for filename in glob.glob(f"{glob.escape(self.lapse_dir)}/*"):
#             os.remove(filename)
#
#
# if __name__ == "__main__":
#     test("video")
