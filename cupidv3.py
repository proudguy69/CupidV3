# this file will be the main runner for EVERYTHING
import asyncio

from Cupidv3Bot.bot import cupidbot
from Cupidv3Bot.settings import TOKEN


from Cupidv3Backend.server import app

def run_flask():
    app.run(debug=True)


def main():
    asyncio.create_task(cupidbot.run(TOKEN))
    

if __name__ == "__main__":
    asyncio.run(main())
    