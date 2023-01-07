import os
import cv2
import glob
import types
import telebot
from telebot import types
from datetime import datetime
from config import timelapse_dir, token, usernames, ids, videourl

dt = str(datetime.now().strftime('%D %H:%M:%S'))
if not os.path.exists(timelapse_dir):
    os.mkdir(timelapse_dir)
bot = telebot.TeleBot(token)


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
            # При выборе параметра "Фото"
            count = 1
            now = datetime.now().strftime('%m-%d  %H-%M-%S')
            filename = f"{timelapse_dir}/{now} foto {count}.jpg"
            bot.send_message(test.chat.id, " через несколько секунд будет фото ")
            vidcap = cv2.VideoCapture(videourl)
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
            # При выборе параметра "Видео"
            bot.send_message(test.chat.id, " через несколько секунд будет видео ")
            height = 1080
            width = 1920
            video = cv2.VideoWriter(timelapse_dir + "video" + ".avi", cv2.VideoWriter_fourcc(*'DIVX'), 3,
                                    (width, height))
            filesforvideo = glob.glob(f"{glob.escape(timelapse_dir)}/*.jpg")
            filesforvideo.sort(key=os.path.getmtime)

            for screenshot in filesforvideo:
                origImage = cv2.imread(screenshot)
                heightOrig, widthOrig, channelsOrig = origImage.shape
                # Изменение разрешения видео
                if height != heightOrig or width != widthOrig:
                    img = cv2.resize(origImage, (width, height))
                    video.write(img)
                else:
                    video.write(origImage)
            video.release()
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


# schedule.every(1).seconds.do(photo)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)


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
