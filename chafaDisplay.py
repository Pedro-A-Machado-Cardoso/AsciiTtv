from chafa import *
from PIL import Image
import json
import cv2

class ChafaDisplay:
    def __init__(self, img, res=10):
        self.config = CanvasConfig()
        self.res = res
        self.config.height = 1080//res
        self.config.width  = 1920//res
        self.canvas = Canvas(self.config)
        self.image = self.fromcv2(img)
        self.height = self.image.height
        self.width = self.image.width
        self.bands  = len(self.image.getbands())
        self.config.calc_canvas_geometry(
            self.image.width,
            self.image.height,
            11/24
        )

    def draw(self):
        self.canvas.draw_all_pixels(
            PixelType.CHAFA_PIXEL_RGB8,
            self.image.tobytes(),
            self.width, self.height,
            self.width * self.bands
        )
        
        return self.canvas.print().decode()
    
    def fromcv2(self, img):
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))