from database.database import BaseDatabaseObject, CONFIGURATION
from discord import Embed

from enum import Enum

class Posting(Enum):
    cases = "posting_cases"
    warn = "posting_warn"
    mod_actions = "posting_mod_actions"



class ChannelPostingConfig:
    def __init__(self, data:dict):
        self.channel_id = data.get()
        self.postings:list[Posting.value] = []
    
    def add_posting(self, posting:Posting):
        self.add_posting(posting.value)

    

class GuildConfig(BaseDatabaseObject):
    def __init__(self, data:dict):
        self._id = data.get('_id')
        self.guild_id = data.get('guild_id')

    async def update(self, data):
        result = await self._update(CONFIGURATION, {"_id":self._id}, data)
        self.__init__(result)
        return result



    @classmethod
    async def create_record(cls, guild_id:int):

        data = {
            "guild_id":guild_id
        }

        record = await BaseDatabaseObject._create_record(CONFIGURATION, data)
        return GuildConfig(record)
    