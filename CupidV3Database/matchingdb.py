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
        self.username = data.get('username')
        self.avatar_url = data.get('avatar_url')
        self.banner_url = data.get('banner_url')
        self.message_id = data.get('message_id')
        self.posted_channel = data.get('posted_channel')
        self.posted_message = data.get('posted_message')
        self.embed = self.create_embed()
        self.__dict__.pop('embed')
    

    async def update(self, data:dict):
        await self._update(MATCHING, {'_id':self._id}, data)
        record = await MATCHING.find_one({'_id':self._id})
        self.__init__(record)

    async def get_compatible_profiles(self) -> list["Profile"]:
        compatible_profiles:list[Profile] = []
        all_profiles = [Profile(record) async for record in MATCHING.find()]
        # only age check for now

        for profile in all_profiles:
            if self.age >= 18:
                if profile.age >= 18:
                    compatible_profiles.append(profile)
            else:
                difference = profile.age - self.age
                if difference >= -2 or difference <= 2:
                    compatible_profiles.append(profile)
        
        return compatible_profiles



    def create_embed(self, color:int=None):
        description = f"""❥﹒User: <@{self.user_id}> | `{self.username}`
        ❥﹒Name: `{self.name}`
        ❥﹒Age: `{self.age}`
        ❥﹒Pronouns: `{self.pronouns}`
        ❥﹒Gender: `{self.gender}`
        ❥﹒Sexuality: `{self.sexuality}`
        ❥﹒Bio: ```{self.bio}```
        """.strip()
        
        embed = Embed(title="Profile", description=description, color=color)
        try:
            embed.set_author(name=self.username, icon_url=self.avatar_url)
        except:
            embed.set_author(name=self.username)
        try:
            embed.set_image(url=self.banner_url)
        except:
            pass

        return embed


    @classmethod
    async def create_profile(cls, user_id:int, name:str, age:str, pronouns:str, gender:str, sexuality:str, bio:str, username:str, avatar_url:str=None, banner_url:str=None):
        record = await MATCHING.find_one({'user_id':user_id})
        if record: return Profile(user_id)
        data = {
            "user_id":user_id,
            "username":username,
            "name":name,
            "age": age,
            "pronouns":pronouns,
            "gender":gender,
            "sexuality":sexuality,
            "bio":bio,
            "avatar_url":avatar_url,
            "banner_url":banner_url
        }
        await cls._create_record(MATCHING, data)
    
    @classmethod
    async def delete_profile(cls, user_id:int):
        await MATCHING.delete_one(filter={'user_id': user_id})
        
    
    @classmethod
    async def get_profile(cls, user_id:int, create_if_not_exists:bool=False, *, name:str='', age:str='', pronouns:str='', gender:str='', sexuality:str='', bio:str='', username:str='',avatar_url:str=None, banner_url:str=None) -> tuple["Profile", bool]:
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
                return await cls.create_profile(user_id, name=name, age=age, pronouns=pronouns, gender=gender, sexuality=sexuality, bio=bio, username=username, avatar_url=avatar_url, banner_url=banner_url), True
            else:
                return None, False
        return Profile(record), False
