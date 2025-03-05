# this will represent a websocket server.
# this will host events and talk the flask server to the discord bot. essentially enabling cross communication.

from websockets.asyncio.server import serve, ServerConnection, ServerProtocol

import asyncio

from discord.utils import setup_logging
import logging
import json

class Server:
    def __init__(self, host='localhost', port=5001):
        setup_logging()
        self.logger = logging.getLogger('Cupidv3Server.server')
        self.host = host
        self.port = port
        self.logger.info(f"Initializing server on ws://{host}:{port}")

    # called when a new connection is made
    async def handler(self, websocket:ServerConnection):
        self.logger.info(f"New Client connected: {websocket.local_address}")
        try:
            async for message in websocket:
                await self.handle_message(message)
        except Exception as exception:
            self.logger.error(f"The following error occured: {exception}")
        finally:
            self.logger.warning(f"Client Closed: {websocket.local_address}")
    

    async def handle_message(self, message):
        data:dict = json.loads(message)
        event = data.get('event')
        self.logger.info(f"new event [{event}]: {message}")
        
        
    async def start(self):
        async with serve(self.handler,self.host,self.port):
            await asyncio.Future()




async def main():
    server = Server()
    await server.start()
    

if __name__ == "__main__":
    asyncio.run(main())