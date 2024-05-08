#This script functions as the sender in a remote microphone streaming setup.
#It captures audio from the system's default microphone using pyaudio, encodes this
#audio data, and sends it over a WebSocket connection to a server. The server
#then relays this data to one or more receivers.
#
#Usage:
#    Execute the script with Python 3.x to begin capturing and streaming audio.
#    The script sends audio data to the WebSocket server specified in WS_URL.
#    If a "panic" message is received from the server, the script stops streaming,
#    closes the audio stream, and exits.

import pyaudio
import websocket
import threading
import logging
import time
from logstash_async.handler import AsynchronousLogstashHandler

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 * 10
stream = None
p = pyaudio.PyAudio()
WS_URL = (
    "ws://3.25.140.218:8765"
)
#local host logging in local file system
log_host = 'localhost'	
# any port that is not common port nor conflicting between sever / sender / receiver
log_port = 1234

# Get a logger, set debug level = info, create and add the handler
swann_logger = logging.getLogger('python-logstash-logger')
swann_logger.setLevel(logging.DEBUG)
async_handler = AsynchronousLogstashHandler(log_host, log_port, database_path=None)
swann_logger.addHandler(async_handler)

def on_message(ws, message):
	swann_logger.info("Received message from server %s %s",message, time.time())
    if message == "panic":
        stream.stop_stream()
        stream.close()
        p.terminate()
		swann_logger.info("Terminated %s", time.time())
        ws.close()



def on_error(ws, error):
	swann_logger.info("%s %s",error, time.time())


def on_open(ws):
    def run(*args):
        global stream
        stream = p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
		swann_logger.info("Recording Started %s", time.time())

        while True:
            data = stream.read(CHUNK)
            ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)

        stream.stop_stream()
        stream.close()
        p.terminate()
		swann_logger.info("Terminated %s", time.time())
        ws.close()

    thread = threading.Thread(target=run)
    thread.start()


if __name__ == "__main__":
    ws = websocket.WebSocketApp(WS_URL, on_message=on_message, on_error=on_error)
    ws.on_open = on_open
    ws.run_forever()
