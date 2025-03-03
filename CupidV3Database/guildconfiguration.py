from CupidV3Database.database import BaseDatabaseObject, CONFIGURATION
from discord import Embed

from Cupidv3Bot.extensions.dispatcher import dispatcher

# channels listen to "events"

# subscribed_events = {
#     "cases_create": [chan_id1,...]
# }


class SubscribedEvents:
    def __init__(self, data:dict):
        self.cases:list[int] = data.get('cases', []) # all cases events
        self.cases_create:list[int] = data.get('cases_create', [])

        self.guild_config:list[int] = data.get('guild_config', []) # ALL Config events
        self.guild_config_edit:list[int] = data.get('guild_config_edit', [])

        self.level_up:list[int] = data.get('level_up', [])

    def add(self, event:str, channel_id:int) -> tuple[bool, str]:
        """adds a channel_id to an event

        Args:
            event (str): the name of the event
            channel_id (int): the channel id to remove

        Returns:
            tuple[bool, str]: True/False if success, str message if not successfull
        """
        success = True
        channel = None
        match (event):
            # case events
            case 'cases_':
                channel = self.cases
            case 'cases_create':
                channel = self.cases_create
            # guild config events
            case 'config_':
                channel = self.guild_config
            case 'config_guild_create':
                channel = self.guild_config_edit
            # level up events
            case 'level_up':
                channel = self.level_up
            case _:
                return False, f'`{event}` doesn\'t exists!'
        
        
        if channel_id in channel:
            return False, f"<#{channel_id}> is already in `{event}`"
        
        channel.append(channel_id)
        return success, f'Successfully added <#{channel_id}> to `{event}`'
    
    def remove(self, event:str, channel_id:int) -> bool:
        """adds a channel_id to an event

        Args:
            event (str): the name of the event
            channel_id (int): the channel id to remove

        Returns:
            tuple[bool, str]: True/False if success, str message if not successfull
        """
        success = True
        channel = None
        match (event):
            # case events
            case 'cases_':
                channel = self.cases
            case 'cases_create':
                channel = self.cases_create
            # guild config events
            case 'config_':
                channel = self.guild_config
            case 'config_guild_create':
                channel = self.guild_config_edit
            # level up events
            case 'level_up':
                channel = self.level_up
            case _:
                return False, f'`{event}` doesn\'t exists!'
        
        
        if channel_id not in channel:
            return False, f"<#{channel_id}> is not in `{event}`"
        
        channel.append(channel_id)
        return success, f'Successfully removed <#{channel_id}> from `{event}`'
        
    
 
    
    

class GuildConfig(BaseDatabaseObject):
    """Represents a base guild object, you dont create this yourself, use the .get_record method
    """
    def __init__(self, data:dict):
        self._id = data.get('_id')
        self.guild_id = data.get('guild_id')
        self.subscribed_events = SubscribedEvents(data.get('subscribed_events', {}))
        

    async def update(self, data):
        """Updates the data using mongodbs update method, this passes in the query for you so all you need to pass in is the mongodb {} udater object
        this also in place re-runs the __init__ method so the object is updated in place with its new values.

        Args:
            data (dict): a dict of the update methods {"$set":{"some_data":0}}

        Returns:
            UpdateResult: the result object of the update
        """
        result = await self._update(CONFIGURATION, {"_id":self._id}, data)
        self.__init__(result)
        return result
    
    
    async def subscribe(self, event:str, channel_id:str):
        """subscribes a channel to an event

        Args:
            event (str): the name of the event
            channel_id (str): the channel id to subscribe the event too
        
        Returns:
            tuple[bool, str]: true on success, message on failure.
        """
        success, msg = self.subscribed_events.add(event, channel_id)
        if success: await self.update({"$set":{"subscribed_events":self.subscribed_events.__dict__}})
        return success, msg
    
    async def unsubscribe(self, event:str, channel_id:str) -> tuple[bool, str]:
        """unsubscribes a channel from an event

        Args:
            event (str): the name of the event
            channel_id (str): the channel id to unsubscribe from the event
        
        Returns:
            tuple[bool, str]: true on success, message on failure.
        """
        success, msg = self.subscribed_events.remove(event, channel_id)
        if success: await self.update({"$set":{"subscribed_events":self.subscribed_events.__dict__}})
        return success, msg





    # idk maybe info about how the thing was updated ?
    async def logger_embed(self):
        config_update_embed = Embed()


    @classmethod
    async def create_record(cls, guild_id:int) -> "GuildConfig":
        """Creates the a record, this is also called by get_record if no records exists so may be useless to you

        Args:
            guild_id (int): The id of the guild you want to init

        Raises:
            RecordExistsException: If the record exists, this exception is called.

        Returns:
            GuildConfig: The new guild config object
        """
        data = await CONFIGURATION.find_one({"guild_id":guild_id}) # see if exists
        if data: raise RecordExistsException(f"Record for {guild_id} already exists")

        data = {
            "guild_id":guild_id,
        }

        record = await BaseDatabaseObject._create_record(CONFIGURATION, data)
        config = GuildConfig(record)
        return GuildConfig(record)

    @classmethod
    async def get_record(cls, guild_id:int) -> "GuildConfig":
        """Gets a guild record or creates one for you if one doesn't exists

        Args:
            guild_id (int): The guild Id of of the guild you want to get the configuration of

        Returns:
            GuildConfig: The guild configuration object you requested
        """
        record = await CONFIGURATION.find_one({"guild_id":guild_id})
        if not record: config = await GuildConfig.create_record(guild_id)
        else: config = GuildConfig(record)
        return config
    
    




# Exceptions
class RecordExistsException(BaseException):
    def __init__(self, *args):
        super().__init__(*args)