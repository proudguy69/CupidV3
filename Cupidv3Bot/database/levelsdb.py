from Cupidv3Bot.database.database import BaseDatabaseObject, LEVELS
from Cupidv3Bot.extensions.dispatcher import dispatcher

from discord import Embed, File
from typing import Union

import asyncio


class Level(BaseDatabaseObject):
    def __init__(self, data:dict):
        self._id = data.get('_id')
        self.guild_id = data.get('guild_id')
        self.user_id = data.get('user_id')
        self.xp = data.get('xp')
        self.level = data.get('level')

    
    async def increase_xp(self, amount:int):
        new_xp = self.xp + amount

        level_up = False
        if new_xp > self.level * 100:
            level_up = True
            new_xp = new_xp % self.level * 100
            self.level +=1
        
        await self.update({"$set":{"xp":new_xp, "level":self.level}})
        if level_up: await dispatcher.dispatch(event_name="level_up", level=self)

    async def get_rank_card(self, username:str, avatar_url:str) -> tuple[Embed, File]:
        from other.imagegeneration import ImageGenerator
        await asyncio.to_thread(ImageGenerator.generate_level_card, self.user_id, username, avatar_url, self.level, self.xp, 1)
        file = File(f'images/{self.user_id}.png', filename=f'{self.user_id}_rank_card.png')
        rank_embed = Embed(title="Rank", color=0xffa6a1)
        rank_embed.set_author(name=f'{username}\'s Rank', icon_url=avatar_url)
        rank_embed.set_image(url=f'attachment://{self.user_id}_rank_card.png')
        return rank_embed, file


    async def update(self, data:dict): 
        new_data = await self._update(LEVELS, {"_id":self._id}, data)
        self.__init__(new_data)
    
    @classmethod
    async def get_level(cls, guild_id:int, user_id:int) -> "Level":
        data = await LEVELS.find_one({"guild_id":guild_id,"user_id":user_id})
        if not data: return await cls.create_level(guild_id, user_id)
        return Level(data)

    @classmethod
    async def create_level(cls, guild_id:int, user_id:int) -> "Level":
        data = await LEVELS.find_one({"guild_id":guild_id,"user_id":user_id})
        if data: return Level(data)

        data = {
            "guild_id": guild_id,
            "user_id": user_id,
            "level": 1,
            "xp":0,
        }

        record = await cls._create_record(LEVELS, data)
        new_level = Level(record)
        return new_level
        

        
        
