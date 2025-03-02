from CupidV3Database.database import BaseDatabaseObject, MODERATION
from discord import Embed

from Cupidv3Bot.extensions.dispatcher import dispatcher

class CaseType:
    warn = "warn"

class Case(BaseDatabaseObject):
    def __init__(self, data:dict):
        self._id = data.get("_id")
        self.guild_id = data.get("guild_id", None)
        self.moderator_id = data.get("moderator_id", None)
        self.moderator_name = data.get("moderator_name", None)
        self.moderator_avatar = data.get("moderator_avatar", None)
        self.target_id = data.get("target_id", None)
        self.target_name = data.get("target_name", None)
        self.target_avatar = data.get("target_avatar", None)
        self.case_type = data.get("case_type", None)
        self.reason = data.get("reason", None)
        self.evidence = data.get("evidence", None)
        self.duration = data.get("duration", None)
        self.embed = self.create_basic_embed()
        super().__init__()
    

    async def update(self, data):
        response = await self._update(MODERATION, {"_id":self._id}, data)
        self.__init__(response)
    
    async def parse_duration(self, duration:str) -> int:
        """parses the string duration in 10h5m23s format to seconds

        Args:
            duration (str): the duration to be converted. Defaults to "10h5m23s".

        Returns:
            int: the total duration in seconds
        """
        multis = {
            "s":1,
            "m":60,
            "h":3600
        }
        total_duration = 0
        current_time = ''
        for character in duration:
            try:
                int(character)
                current_time += f'{character}'
            except: 
                total_duration += int(current_time) * multis[character]
                current_time = ''
        return total_duration
    
    def create_basic_embed(self) -> Embed:
        description = f"""
        Target: <@{self.target_id}>
        Moderator: <@{self.moderator_id}>
        """
        case_embed = Embed(title=f"Case #{self._id}",description=description, color=0xFDFD96)
        case_embed.add_field(name="Reason", value=self.reason)
        case_icon = self.target_avatar if self.target_avatar else None
        case_embed.set_author(name=self.target_name, icon_url=case_icon)
        case_embed.set_thumbnail(url=case_icon)
        return case_embed


    @classmethod
    async def create_record(cls, guild_id:int, moderator_id:int, moderator_name:str, moderator_avatar:str, target_id:int, target_name:str, target_avatar:str, case_type:CaseType, reason:str="None Provided", evidence:list=None, duration:str=None) -> "Case":
        
        data = {
            "guild_id":guild_id,
            "moderator_id":moderator_id,
            "moderator_name":moderator_name,
            "moderator_avatar":moderator_avatar,
            "target_id":target_id,
            "target_name":target_name,
            "target_avatar":target_avatar,
            "case_type":case_type,
            "reason":reason,
            "evidence":evidence,
            "duration":duration,
        }

        record = await BaseDatabaseObject._create_record(MODERATION, data)
        new_case = Case(record)
        await dispatcher.dispatch(event_name="cases_create", new_case=new_case)
        return new_case
        




