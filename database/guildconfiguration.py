from database.database import BaseDatabaseObject, CONFIGURATION
from discord import Embed

from enum import Enum



# channels listen to "events"

# registered_channels = {
#     channel_id: {
#         "listen":["cases"]
#     }
# }


    

class GuildConfig(BaseDatabaseObject):
    def __init__(self, data:dict):
        self._id = data.get('_id')
        self.guild_id = data.get('guild_id')
        self.registered_channels = data.get('registered_channels', {})

    async def update(self, data):
        result = await self._update(CONFIGURATION, {"_id":self._id}, data)
        self.__init__(result)
        return result
    
    async def add_channel(self, channel_id):
        await self.update({"$set":{f"registered_channels.{channel_id}":{"listen":[]}}})




    @classmethod
    async def create_record(cls, guild_id:int):

        data = {
            "guild_id":guild_id
        }

        record = await BaseDatabaseObject._create_record(CONFIGURATION, data)
        return GuildConfig(record)

    @classmethod
    async def get_record(cls, guild_id:int):
        record = await CONFIGURATION.find_one({"guild_id":guild_id})
        if not record: record = await GuildConfig.create_record(guild_id)
        return GuildConfig(record)
    