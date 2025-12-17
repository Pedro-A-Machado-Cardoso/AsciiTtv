import streamlink
import cv2
from videoscreenshot import VideoScreenshot
import time
import json

def stream_to_url(url, quality='best'):
    streams = streamlink.streams(url)
    if streams:
        return streams[quality].to_url()
    else:
        raise ValueError("No streams were available.")

channel_url = f"www.twitch.tv/{json.dumps(json.loads(open("config.json", "r+").read())["streamer"])}"
framecount = 0
try:
    stream_url = stream_to_url(channel_url, 'best')
    capObj = VideoScreenshot(stream_url)
    cap = capObj.capture
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    if not cap.isOpened():
        raise IOError("Cannot open video stream.")
    print("Stream starting in 5!")
    time.sleep(5)
    while True:
        framecount += 1

        capObj.show_frame()

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(framecount)
            break

    cap.release()
    cv2.destroyAllWindows()

except ValueError as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")