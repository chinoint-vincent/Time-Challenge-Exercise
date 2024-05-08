#This script is the receiver component of a remote microphone streaming system.
#It connects to a specified WebSocket server, receives audio data streamed from a sender,
#and plays it back in real-time. It uses pyaudio for audio playback and numpy for
#manipulation of the audio data.
#
#Usage:
#    Run the script with Python 3.x. It will automatically connect to the WebSocket server
#    specified in the WS_URL variable and start playing received audio data.
#    To stop the script, focus on the terminal and press Ctrl+C.
#

import pyaudio
import websocket
import threading
import numpy as np
import logging
import time
from logstash_async.handler import AsynchronousLogstashHandler

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 * 10
#local host logging in local file system
log_host = 'localhost'	
# any port that is not common port nor conflicting between sever / sender / receiver
log_port = 3456

# Get a logger, set debug level = info, create and add the handler
swann_logger = logging.getLogger('python-logstash-logger')
swann_logger.setLevel(logging.DEBUG)
async_handler = AsynchronousLogstashHandler(log_host, log_port, database_path=None)
swann_logger.addHandler(async_handler)

# WebSocket
WS_URL = (
    "ws://audioendpoint.yourserver.com/ws?password=demopassword"
)


def on_message(ws, message):
    # Convert the message data to a numpy array of the correct type
    data = np.frombuffer(message, dtype=np.int16)
    stream.write(data.tobytes())


def on_error(ws, error):
	swann_logger.info("This is an info message at %s", time.time())

def on_open(ws):
	swann_logger.info("This is an info message at %s", time.time())

def send_panic_and_exit():
	swann_logger.info("This is an info message at %s", time.time())
    ws.send("panic")
    ws.close()
    stream.stop_stream()
    stream.close()
    p.terminate()
	swann_logger.info("This is an info message at %s", time.time())
    exit()

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        WS_URL, on_message=on_message, on_error=on_error
    )
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        output=True,
        frames_per_buffer=CHUNK,
    )

    wst = threading.Thread(target=lambda: ws.run_forever())
    wst.daemon = True
    wst.start()

	swann_logger.info("Receiving... Press Ctrl+C to stop %s", time.time())
    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        send_panic_and_exit()
