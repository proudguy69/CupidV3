from database.database import BaseDatabaseObject, CONFIGURATION
from discord import Embed

from pydantic import BaseModel, Field
from typing import Union, Optional


from enum import Enum



# channels listen to "events"

# registered_channels = {
#     channel_id: {
#         "listen":["cases"]
#     }
# }


class Event:
    add = 'add'
    remove = 'remove'

class Channel:
    def __init__(self, data:dict):
        self.channel_id = data.get('channel_id')
        self.listen:list[str] = data.get('listen')
        self.index = data.get('index')
    
    def __repr__(self):
        return str(self.__dict__)

    def add_listen(self, type):
        self.listen.append(type)

    def remove_listener(self, type):
        self.listen.remove(type)
    
    def to_dict(self):
        return {"channel_id":self.channel_id,"listen":self.listen,"index":self.index}
    
    @classmethod
    def new(cls, channel_id, listen:str):
        return Channel({"channel_id":channel_id, "listen":[listen], "index":None})
        

class RegisteredChannels:
    def __init__(self, data:list[dict]):
        self.channels:list[Channel] = [Channel(channel) for channel in data]
    
    def __repr__(self):
        return str(self.__dict__)
    
    def dict_channels(self):
        return [c.to_dict() for c in self.channels]
    
    def add_channel(self, channel:Channel):
        channel.index = len(self.channels)
        self.channels.append(channel)

    

class GuildConfig(BaseDatabaseObject):
    def __init__(self, data:dict):
        self._id = data.get('_id')
        self.guild_id = data.get('guild_id')
        self.registered_channels = RegisteredChannels(data.get("registered_channels", []))

    async def update(self, data):
        result = await self._update(CONFIGURATION, {"_id":self._id}, data)
        self.__init__(result)
        return result
    
    async def add_channel(self, channel:Channel):
        # if channel already exists and is added return
        for r_channel in self.registered_channels.channels:
            if r_channel.channel_id == channel.channel_id: return
        self.registered_channels.add_channel(channel)
        await self.update({"$set":{"registered_channels":list(self.registered_channels.dict_channels())}})

    
    async def update_channel(self, channel:Channel, event:Event, data:str):
        for r_channel in self.registered_channels.channels:
            if channel.channel_id == r_channel.channel_id:
                if event == Event.add:
                    r_channel.add_listen(data)
                elif event == Event.remove:
                    r_channel.remove_listener(data)
        
        await self.update({"$set":{"registered_channels":list(self.registered_channels.dict_channels())}})





    @classmethod
    async def create_record(cls, guild_id:int):
        data = await CONFIGURATION.find_one({"guild_id":guild_id}) # see if exists
        if data: return GuildConfig(data)

        data = {
            "guild_id":guild_id,
            "registered_channels":[]
        }

        record = await BaseDatabaseObject._create_record(CONFIGURATION, data)
        return GuildConfig(record)

    @classmethod
    async def get_record(cls, guild_id:int):
        record = await CONFIGURATION.find_one({"guild_id":guild_id})
        if not record: record = await GuildConfig.create_record(guild_id)
        return GuildConfig(record)
    