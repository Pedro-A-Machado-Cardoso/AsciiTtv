import queue
from threading import Thread
import cv2
from ascii import Ascii
import json
from rich.live import Live
from rich.console import Console
from rich.text import Text


class VideoScreenshot(object):
    def __init__(self, src=0):
        self.colored = json.loads(open('config.json', 'r+', encoding='utf-8').read())['colored']
        # Create a VideoCapture object
        self.capture = cv2.VideoCapture(src)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        self.capture.set(cv2.CAP_PROP_FPS, 20)

        self.frame_queue = queue.Queue(maxsize=1)
        self.latest = None

        # Default resolutions of the frame are obtained (system dependent)
        self.frame_width = int(self.capture.get(3))
        self.frame_height = int(self.capture.get(4))

        # Start the thread to read frames from the video stream
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.asciiQ = queue.Queue(maxsize=1)

    def update(self):
        # Read the next frame from the stream in a different thread
        while self.capture.isOpened():
            (self.status, self.frame) = self.capture.read()
            if not self.status:
                continue
            # Drop old frame if queue is full
            if self.frame_queue.full():
                try:
                    while self.frame_queue.qsize() > 0:
                        self.frame_queue.get()
                except queue.Empty:
                    pass

            self.frame_queue.put_nowait(self.frame)
            self.latest = self.frame

    def renderToAscii(self):
        while self.capture.isOpened():
            qframe = self.frame_queue.get()
            frame = Ascii(qframe)
            frame = frame.imgToAscii(self.colored)
            if self.asciiQ.qsize() > 0:
                self.asciiQ.get_nowait()
            self.asciiQ.put_nowait(frame)

    def show_frame(self):
        console = Console()
        try:

            self.asciiThread = Thread(target=self.renderToAscii, args=())
            self.asciiThread.daemon = True
            self.asciiThread.start()
            with Live("", console=console, refresh_per_second=20, screen=True) as live:
                while True:
                    if self.status:
                        if self.asciiQ.qsize() > 0:
                            text = self.asciiQ.get()
                            if self.colored:
                                live.update(Text.from_ansi(text))
                            else:
                                live.update(text)

        except queue.Empty:
            print("H")