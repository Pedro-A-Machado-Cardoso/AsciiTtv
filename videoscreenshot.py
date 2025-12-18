import queue
from threading import Thread
import cv2
from ascii import Ascii
import json
from rich.live import Live
from rich.console import Console
from rich.text import Text
import time
from chafaDisplay import ChafaDisplay


class Display(object):
    def __init__(self, src=0):
        self.colored = json.loads(open('config.json', 'r+', encoding='utf-8').read())['colored']
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src, cv2.CAP_FFMPEG)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.capture.set(cv2.CAP_PROP_FPS, 60)

        self.frame_queue = queue.Queue(maxsize=1)
        self.latestTime = 0

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.asciiQ = queue.Queue(maxsize=1)
        self.status = None

        # Chafa
        self.display = None

    def update(self):
        # Read the next frame from the stream in a different thread
        while self.capture.isOpened():
            self.capture.grab()
            # Drop old frame if queue is full
            now = time.monotonic()
            if now - self.latestTime >= 1/30:
                ret, frame = self.capture.retrieve()
                self.status = ret
                if ret:
                    self.frame = frame
                    self.latestTime = now
                    self.frame_queue.put(self.frame)
            
            if self.frame_queue.full():
                try:
                    while self.frame_queue.qsize() > 0:
                        self.frame_queue.get()
                except queue.Empty:
                    pass
                

    def renderToAscii(self):
        while self.capture.isOpened():
            qframe = self.frame
            frame = Ascii(qframe)
            frame = frame.imgToAscii(self.colored)
            if self.asciiQ.qsize() > 100:
                self.asciiQ.get()
            self.asciiQ.put(frame)

    def show_frame(self):
        console = Console(
            force_terminal=True,
            markup=False,
            highlight=False,
            emoji=False
        )
        
        usechafa = int(json.loads(open('config.json', 'r+', encoding='utf-8').read())['usechafa'])
        try:
            if not usechafa:
                self.asciiThread = Thread(target=self.renderToAscii, args=())
                self.asciiThread.daemon = True
                self.asciiThread.start()
                with Live("", console=console, refresh_per_second=10, screen=True) as live:
                    while True:
                        if self.status:
                            if self.asciiQ.qsize() > 0:
                                text = self.asciiQ.get()
                                if self.colored:
                                    live.update(Text.from_ansi(text))
                                else:
                                    live.update(text)
                                time.sleep(.1)
            else:
                self.chafaThread = Thread(target=self.chafaDisplay, args=(int(json.dumps(json.loads(open("config.json", "r", encoding='utf-8').read())["resolution"])),))
                self.chafaThread.daemon = True
                self.chafaThread.start()
                with Live("", console=console, refresh_per_second=60, screen=True) as live:
                    while True:
                        if self.status:
                            if self.display:
                                live.update(Text.from_ansi(self.display))

        except queue.Empty:
            print("Queue empty!")

    def chafaDisplay(self, res):
        while self.capture.isOpened():
            frame = self.frame.copy()
            self.display = ChafaDisplay(frame, res).draw()
            # time.sleep(0.5)
        