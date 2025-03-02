import asyncio
from Cupidv3Bot.bot import cupidbot
from Cupidv3Bot.settings import TOKEN


def main():
    asyncio.create_task(cupidbot.run(TOKEN))
    

if __name__ == "__main__":
    asyncio.run(main())
    