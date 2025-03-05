import asyncio

import threading

from Cupidv3Backend.server import app
from Cupidv3Server.flaskclient import Client


async def main():
    client = Client()
    await app.set_client(client)
    t = threading.Thread(target=client.start)
    t.start()

    app.run(debug=True)
    

if __name__ == "__main__":
    asyncio.run(main())
    