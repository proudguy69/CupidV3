# this will serve as a client for the flask server to communicate wit hthe bot client
from websockets.asyncio.client import connect, ClientConnection
from websockets.exceptions import ConnectionClosed
import asyncio



import threading

from discord.utils import setup_logging
import logging

import json

class Client:
    def __init__(self, uri='ws://localhost:5001'):
        setup_logging()
        self.logger = logging.getLogger('flaskclient.Client')
        self.uri = uri
        self.logger.info(f"Initializing client connection to {uri}")
        self.events = {}
        self.ws:ClientConnection = None
        self.close_signal = False
        

    async def connect(self):
        async with connect(self.uri) as websocket:
            if self.close_signal: return
            self.ws = websocket
            await asyncio.gather(self.recv_messages(websocket))

    async def recv_messages(self, websocket:ClientConnection):
        try:
            async for message in websocket:
                if self.close_signal: break
                data = json.loads(message)
        except ConnectionClosed:
            self.logger.warning('Connection Closed')

    async def emit(self, data:dict):
        package = json.dumps(data)
        await self.ws.send(package)

    async def close(self):
        self.ws.close(code=1000, reason='I want to close')
        self.close_signal = True


    def start(self):
        try:
            asyncio.run(self.connect())
        except:
            pass
        



    

#client = Client()