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
        

    async def connect(self):
        async with connect(self.uri) as websocket:
            self.ws = websocket
            await asyncio.gather(self.recv_messages(websocket))

    async def recv_messages(self, websocket:ClientConnection):
        try:
            async for message in websocket:
                data = json.loads(message)
        except ConnectionClosed:
            self.logger.warning('Connection Closed')

    async def emit(self, data:dict):
        package = json.dumps(data)
        await self.ws.send(package)

    def start(self):
        asyncio.run(self.connect())
        



    

#client = Client()