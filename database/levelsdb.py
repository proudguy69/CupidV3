from database.database import BaseDatabaseObject, LEVELS



class Level(BaseDatabaseObject):
    def __init__(self, data:dict):
        self._id = data.get('_id')
        self.guild_id = data.get('guild_id')
        self.username = data.get('username')
        