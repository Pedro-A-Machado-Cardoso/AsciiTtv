import cv2
import numpy as np
import math
import json
import sys

class Ascii:
    def __init__(self, img: cv2.typing.MatLike, res=json.dumps(json.loads(open("config.json", "r+").read())["resolution"])):
        self.res = res
        self.img = img
        self.height, self.width, self.channels = self.img.shape
        self.colors = json.dumps(json.loads(open("config.json", "r+").read())["tileset"])
        self.ascii = ""
    
    def pixelClamp(self, x : int, y : int):
        try:
            pixel = self.img[x, y]
        except:
            return len(self.colors)
        levels = len(self.colors)
        avg = (pixel[0] + pixel[1] + pixel[2])/3
        clamp = levels - round(avg/levels) - 1
        return clamp
    
    def imgToAscii(self):
        ascii = ""
        for h in range(math.floor(self.height/self.res)):
            for w in range(math.floor(self.width/self.res)):
                clamp = self.pixelClamp(h*self.res - 1, w*self.res - 1)
                ascii += self.colors[clamp]
            ascii += "\n"
        ascii.removesuffix("\n")
        self.ascii = ascii
        return ascii
    
    def printAscii(self):
        split = self.ascii.split("\n")
        
        for i in split:
            sys.stdout.write(i + "\n")
            sys.stdout.flush()
            
    


    