from CupidV3Database.database import BaseDatabaseObject, MATCHING
from discord import Embed


class Profile(BaseDatabaseObject):
    def __init__(self, data:dict):
        self._id = data.get('_id')
        self.user_id = data.get('user_id')
        self.name = data.get('name')
        self.age = data.get('age')
        self.pronouns = data.get('pronouns')
        self.gender = data.get('gender')
        self.sexuality = data.get('sexuality')
        self.bio = data.get('bio')
        self.embed = self.create_embed()
    

    async def update(self, data:dict):
        await self._update(MATCHING, {'_id':self._id}, data)
        record = await MATCHING.find_one({'_id':self._id})
        self.__init__(record)

    def create_embed(self, color:int=None):
        description = f"""
        ❥﹒User: <@{self.user_id}>
        ❥﹒Name: {self.name}
        ❥﹒Age: {self.age}
        ❥﹒Pronouns: {self.pronouns}
        ❥﹒Gender: {self.gender}
        ❥﹒Sexuality: {self.sexuality}
        ❥﹒Bio: ```{self.bio}```
        """
        embed = Embed(title="Profile", description=description, color=color)
        return embed


    @classmethod
    async def create_profile(cls, user_id:int, name:str, age:str, pronouns:str, gender:str,sexuality:str,bio:str):
        record = await MATCHING.find_one({'user_id':user_id})
        if record: return Profile(user_id)
        data = {
            "user_id":user_id,
            "name":name,
            "age": age,
            "pronouns":pronouns,
            "gender":gender,
            "sexuality":sexuality,
            "bio":bio,
        }
        await cls._create_record(MATCHING, data)
    
    @classmethod
    async def delete_profile(cls, user_id:int):
        await MATCHING.delete_one(filter={'user_id': user_id})
        
    
    @classmethod
    async def get_profile(cls, user_id:int, create_if_not_exists:bool=False, *, name:str='', age:str='', pronouns:str='', gender:str='', sexuality:str='', bio:str='') -> tuple["Profile", bool]:
        """gets a profile, creates one with the values provided if provided

        Args:
            user_id (int): the id of the users profile to get.
            create_if_not_exists (bool): set true if you want to create the profile if its not found.
            name (str, optional): the name of the profile if creating. Defaults to ''.
            age (str, optional): the nageame of the profile if creating. Defaults to ''.
            pronouns (str, optional): the pronouns of the profile if creating. Defaults to ''.
            gender (str, optional): the gender of the profile if creating. Defaults to ''.
            sexuality (str, optional): the sexuality of the profile if creating. Defaults to ''.
            bio (str, optional): the bio of the profile if creating. Defaults to ''.

        Returns:
            tuple[Profile, bool]: the profile of the user, and true if a profile was created
        """
        record = await MATCHING.find_one({'user_id':user_id})
        if not record:
            if create_if_not_exists:
                return await cls.create_profile(user_id, name=name, age=age, pronouns=pronouns, gender=gender, sexuality=sexuality, bio=bio), True
            else:
                return None, False
        return Profile(record), False
