
from PIL import Image 
import sys


class ShowQRcode:
    def __init__(self, image, width=50, height=50):
        self.image = image
        self.width = width
        self.height = height

    def show(self):
        im = Image.open(self.image)
        im = im.resize((self.width, self.height), Image.NEAREST)
        text = ''
        for w in range(self.width):
            for h in range(self.height):
                res = im.getpixel((h, w))
                text += '██' if res == 0 else '  '
            text += '\n'
        return text

if __name__ == '__main__':
    q = ShowQRcode('Qrcode.jpg')
    print(q.show())
