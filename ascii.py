import cv2
import numpy as np
import math
import json
import sys
import colorama
from colorama import Fore

class Ascii:
    def __init__(self, img: cv2.typing.MatLike, res=int(json.dumps(json.loads(open("config.json", "r", encoding='utf-8').read())["resolution"]))):
        self.res = res
        self.img = img
        self.height, self.width, self.channels = self.img.shape
        self.colors = json.loads(open("config.json", "r", encoding='utf-8').read())["tileset"]
        self.ascii = ""

    def getClosestColor(self, pixel):
        r = pixel[2]
        g = pixel[1]
        b = pixel[0]
        rgb = [Fore.BLACK, Fore.RED, Fore.BLUE , Fore.MAGENTA, Fore.GREEN, Fore.YELLOW, Fore.CYAN, Fore.WHITE]
        index = 0
        if r > 69: # Do not blame me
            index += 1
        if b > 69:
            index += 2
        if g > 69:
            index += 4
        return rgb[index]
    
    def pixelClamp(self, x : int, y : int, colored=False):
        try:
            pixel = self.img[x, y]
        except:
            return len(self.colors)
        levels = len(self.colors)
        avg = (pixel[0] + pixel[1] + pixel[2])/3
        clamp = levels - round(avg/levels) - 1
        if colored:
            return self.getClosestColor(pixel) + self.colors[clamp]
        else:
            return self.colors[clamp]
    
    def imgToAscii(self, colored=False):
        colorama.init(autoreset=True)
        ascii = ""
        # print(self.colors.encode("utf-8"))
        for h in range(math.floor(self.height/self.res)):
            for w in range(math.floor(self.width/self.res)):
                symbol = self.pixelClamp(h*self.res - 1, w*self.res - 1, colored)
                ascii += symbol
            ascii += "\n"
        ascii.removesuffix("\n")
        self.ascii = ascii
        return ascii
    
    def printAscii(self):
        split = self.ascii.split("\n")
        
        for i in split:
            sys.stdout.write(i + "\n")
            sys.stdout.flush()
            
    


    