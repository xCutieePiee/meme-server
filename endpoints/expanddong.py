from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji
from math import ceil
from os import listdir


@setup
class ExpandDong(Endpoint):
    params = ['text']
    MAX_WIDTH = 1280

    def generate(self, avatars, text, usernames, kwargs):
        text = text[:200]
        lines = ceil((len(text) * 128) / 1920)
        base = Image.new('RGB', (1920, lines * 128), 'White')
        line = 0
        pos = 0
        chars = dict()
        for i in listdir('assets/expanddong'):
            if i.endswith('.bmp'):
                chars[i[0]] = Image.open(f'assets/expanddong/{i}')
        for char in text:
            char = char.lower()
            if chars.get(char):
                base.paste(chars[char], (pos * 128, line * 128))
            pos += 1
            if pos == 15:
                pos = 0
                line += 1


        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
