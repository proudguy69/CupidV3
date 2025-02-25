from database.database import BaseDatabaseObject, CONFIGURATION
from discord import Embed

from enum import Enum

class Posting(Enum):
    cases = "posting_cases"
    cases_creation = "posting_cases_creation"
    warn = "posting_warn"
    mod_actions = "posting_mod_actions"



class ChannelPostingConfig:
    def __init__(self, channel_id:int, postings:list[str]=[]):
        self.channel_id = channel_id
        self.postings:list[Posting.value] = postings
        self.data = {
            str(self.channel_id): self.postings
        }
    
    def add_posting(self, posting:Posting):
        self.postings.append(posting.value)
        self.__init__(self.channel_id, self.postings)


    

class GuildConfig(BaseDatabaseObject):
    def __init__(self, data:dict):
        self._id = data.get('_id')
        self.guild_id = data.get('guild_id')
        self.channel_configurations = data.get('channel_configurations', [])

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

    @classmethod
    async def get_record(cls, guild_id:int):
        record = await CONFIGURATION.find_one({"guild_id":guild_id})
        if not record: record = await GuildConfig.create_record(guild_id)
        return GuildConfig(record)
    