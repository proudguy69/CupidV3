from discord.ext.commands import Bot
import logging
import asyncio

class Dispatcher:
    def __init__(self, bot:Bot=None):
        self.bot = bot
        self.logger = logging.getLogger('Cupidv3.Dispatcher')
        self._events = {}
    
    def listen(self, event_name):
        # register a listener
        def decorator(func):
            if event_name not in self._events:
                self._events[event_name] = []
            self._events[event_name].append(func)
            return func
        return decorator
    
    async def dispatch(self, event_name, *args, **kwargs):
        if event_name in self._events:
            for func in self._events[event_name]:
                if asyncio.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    func(*args, **kwargs)
    
    def set_bot(self, bot:Bot):
        self.bot = bot


dispatcher = Dispatcher()
