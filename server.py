#
#A WebSocket server designed to relay audio data from a sender to a receiver
#in a remote microphone streaming system. It uses aiohttp to handle WebSocket
#connections. The server listens for incoming audio data on a specified port, 
#and forwards audio data to all connected and authenticated receiver clients.
#
#Usage:
#    Start the server by running this script with Python 3.x. It will listen for
#    connections on 0.0.0.0 at the port defined at the bottom of the script.
#    Senders and receivers connect to this server using the WebSocket protocol,
#    allowing for real-time audio streaming from the sender to the receiver.
#

import asyncio
from aiohttp import web
import logging
import time
from logstash_async.handler import AsynchronousLogstashHandler

# Set of connected WebSocket clients
connected = set()

#local host logging in local file system
log_host = 'localhost'	
# any port that is not common port nor conflicting between sever / sender / receiver
log_port = 2345

# Get a logger, set debug level = info, create and add the handler
swann_logger = logging.getLogger('python-logstash-logger')
swann_logger.setLevel(logging.DEBUG)
async_handler = AsynchronousLogstashHandler(log_host, log_port, database_path=None)
swann_logger.addHandler(async_handler)

async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

	swann_logger.info("A new client connected. %s", time.time())
    connected.add(ws)

    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            # Broadcast incoming text message to all connected websockets
            for socket in connected:
                if socket != ws:
                    await socket.send_str(msg.data)
        elif msg.type == web.WSMsgType.BINARY:
            # Broadcast incoming binary message to all connected websockets
            for socket in connected:
                if socket != ws:
                    try:
                        await socket.send_bytes(msg.data)
                    except Exception as e:
                        pass
        elif msg.type == web.WSMsgType.ERROR:
			swann_logger.info("ws connection closed with exception %s %s", ws.exception(), time.time())

	swann_logger.info("Client disconnected. %s", time.time())
    connected.remove(ws)
    return ws


async def init_app():
    app = web.Application()
    app.add_routes([web.get("/ws", websocket_handler)])
    return app


loop = asyncio.get_event_loop()
app = loop.run_until_complete(init_app())

web.run_app(app, host="3.25.140.218", port=8765) # Swann server host and port settings 
