from streamlink import Streamlink
import colorama
from videoscreenshot import VideoScreenshot
import time
import json

def stream_to_url(url, quality='480p'):
    session = Streamlink()
    session.set_option("twitch-low-latency", True)

    # HLS buffering control
    session.set_option("hls-live-edge", 1)
    session.set_option("hls-segment-threads", 1)

    # Optional but recommended
    session.set_option("ringbuffer-size", 16 * 1024 * 1024)
    streams = session.streams(url)
    session.set_option("twitch-low-latency", True)

    # HLS buffering control
    session.set_option("hls-live-edge", 1)
    session.set_option("hls-segment-threads", 1)

    # Optional but recommended
    session.set_option("ringbuffer-size", 16 * 1024 * 1024)
    if streams:
        return streams[quality].to_url()
    else:
        raise ValueError("No streams were available.")

colorama.init(autoreset=True)
streamer = json.dumps(json.loads(open('config.json', 'r+', encoding='utf-8').read())['streamer']).replace('"', "")
channel_url = f"www.twitch.tv/{streamer}"
framecount = 0
try:
    stream_url = stream_to_url(channel_url, 'best')

    capObj = VideoScreenshot(stream_url)
    cap = capObj.capture
    if not cap.isOpened():
        raise IOError("Cannot open video stream.")
    print("Stream starting in 5!")
    time.sleep(5)
    try:
        capObj.show_frame()
    except Exception as e:
        print(f"Error! {e}")

except ValueError as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")