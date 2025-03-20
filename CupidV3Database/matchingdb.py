from CupidV3Database.database import BaseDatabaseObject, MATCHING
from discord import Embed


class Filters:
    def __init__(self, data:dict, age:int):
        self.age:list[int] = data.get('age', [int(age)-2, int(age)+2])

    @classmethod
    def check_age_compatibility(cls, profile:"Profile", age:int):
        age_filters = profile.filters.age

        min_age = age_filters[0]
        max_age = age_filters[1]

        if age > max_age or age < min_age: return False

        return True

    @classmethod
    def check_compatibility(cls, profile_a:"Profile", profile_b:"Profile"):
        """returns true if profile_a is compatible with profile_b

        Args:
            profile_a (Profile): the profile to run the check on
            profile_b (Profile): the profile to check compatibility for

        Returns:
            bool: true if a is compatible with b
        """
        selected_check = profile_b.user_id not in profile_a.matched_profiles
        rejected_check = profile_b.user_id not in profile_a.rejected_profiles
        user_check = profile_a.user_id != profile_b.user_id
        age_check = cls.check_age_compatibility(profile_a, profile_b.age)


        if age_check and user_check and selected_check and rejected_check: return True
        else: return False


    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(self.__dict__)


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
        self.message_id = data.get('message_id')
        self.posted_channel = data.get('posted_channel')
        self.posted_message = data.get('posted_message')
        self.matched_profiles = data.get('matched_profiles', [])
        self.rejected_profiles = data.get('rejected_profiles', [])
        self.matches = data.get('matches', [])
        self.matched_us = data.get('matched_us', [])
        self.filters = Filters(data.get('filters', {}), self.age)
        self.data = data
    

    async def update(self, data:dict):
        await self._update(MATCHING, {'_id':self._id}, data)
        record = await MATCHING.find_one({'_id':self._id})
        self.__init__(record)

    async def get_compatible_profiles(self) -> list["Profile"]:
        compatible_profiles:list[Profile] = []
        all_profiles = [Profile(record) async for record in MATCHING.find({'approved':True})]

        return all_profiles
        for profile in all_profiles:
            if profile.user_id == self.user_id: continue
            if not Filters.check_compatibility(self, profile): continue
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
    
    async def match(self, other_profile:"Profile"):
        await self.update({"$push":{'matched_profiles':other_profile.user_id}})
        await other_profile.update({"$push":{'matched_us':self.user_id}})
        # * check for match condition
        if self.user_id not in other_profile.matched_profiles: return False
        await self.update({"$push":{'matches':other_profile.user_id}})
        await other_profile.update({"$push":{'matches',self.user_id}})
        return True
    
    async def reject(self, other_profile_id:int):
        await self.update({"$push":{'rejected_profiles':other_profile_id}})

         


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
