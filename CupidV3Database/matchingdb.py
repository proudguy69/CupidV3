from CupidV3Database.database import BaseDatabaseObject, MATCHING


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
    async def get_profile(cls, user_id:int):
        record = await MATCHING.find_one({'user_id':user_id})
        if not record: return None
        return Profile(record)
