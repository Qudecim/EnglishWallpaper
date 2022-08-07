from PIL import Image, ImageDraw, ImageFont
from threading import Thread
import json
import random
import numpy as np
import ctypes
import os
import sys
import time
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
imagePath = os.path.dirname(sys.argv[0]) + "/" + config['general']['OutputImage']
array_words = []
words_count = 0


with open(config['general']['WordsFile'], 'r', encoding='utf-8') as file:
    data_json = file.read()
    array_words = (json.loads(data_json))
    size = 1
    for dim in np.shape(array_words): size *= dim
    words_count = dim


def get_word():
    index_item = random.randint(0, words_count)
    return array_words[index_item]


def draw(word):
    with Image.open("main.png").convert("RGBA") as base:
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        width, height = txt.size
        d = ImageDraw.Draw(txt)

        en_rgba = config['words']['En_RGBA'].split(',')
        ru_rgba = config['words']['Ru_RGBA'].split(',')
        fnt = ImageFont.truetype(config['general']['Font'], int(config['words']['FontSize']))
        d.text(
            (width / 2, height / 2 + int(config['words']['Offset']) + int(config['words']['OffsetFromMiddle'])),
            word['en'],
            font=fnt,
            fill=(int(en_rgba[0]), int(en_rgba[1]), int(en_rgba[2]), int(en_rgba[3])),
            anchor="mm")
        d.text(
            (width / 2, height / 2 + int(config['words']['OffsetFromMiddle'])),
            word['ru'],
            font=fnt,
            fill=(int(ru_rgba[0]), int(ru_rgba[1]), int(ru_rgba[2]), int(ru_rgba[3])),
            anchor="mm")

        en_rgba = config['description']['En_RGBA'].split(',')
        ru_rgba = config['description']['Ru_RGBA'].split(',')
        fnt = ImageFont.truetype(config['general']['Font'], int(config['description']['FontSize']))
        d.text(
            (width / 2, height + int(config['description']['Offset']) + int(config['description']['OffsetFromBottom'])),
            word['desc_en'],
            font=fnt,
            fill=(int(en_rgba[0]), int(en_rgba[1]), int(en_rgba[2]), int(en_rgba[3])),
            anchor="mm")
        d.text(
            (width / 2, height + int(config['description']['OffsetFromBottom'])),
            word['desc_ru'],
            font=fnt,
            fill=(int(ru_rgba[0]), int(ru_rgba[1]), int(ru_rgba[2]), int(ru_rgba[3])),
            anchor="mm")

        out = Image.alpha_composite(base, txt)

        out.save(config['general']['OutputImage'], config['general']['OutputImageType'])
        # out.show()


def change_wallpaper():
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 3)


def my_timer():
    while True:
        draw(get_word())
        change_wallpaper()
        time.sleep(int(config['general']['TimeOut']))


th = Thread(target=my_timer)
th.start()
