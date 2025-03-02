from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.cursor import AsyncCursor

client = AsyncMongoClient("mongodb://localhost:27017")
DATABASE = client.get_database("cupidv3")
MODERATION = DATABASE.get_collection("moderation")
CONFIGURATION = DATABASE.get_collection("configuration")
LEVELS = DATABASE.get_collection("levels")



class BaseDatabaseObject:
    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
    

    async def _update(self,_collection:AsyncCollection, query, data:dict):
        await _collection.update_one(query, data, upsert=True)
        record = await _collection.find_one(query)
        return record

    @classmethod
    async def _get_cursor_size(cls, cursor:AsyncCursor):
        """loops over and counts all records in a cursor obj

        Args:
            cursor (AsyncCursor): the async cusor of a colletion

        Returns:
            int: the size of the cursor
        """
        size = 0
        async for _ in cursor:
            size+=1
        return size


    @classmethod
    async def _create_record(cls, _collection:AsyncCollection, data:dict):
        """creates a base database record, automatically creates _id

        Args:
            _collection (AsyncCollection): the collection to create the record on
            data (dict): the data to insert

        Returns:
            dict: the inserted record
        """
        _id = await BaseDatabaseObject._get_cursor_size(_collection.find()) +1      # calculate size
        data['_id'] = _id                                                           # store the _id 
        await _collection.insert_one(data)                                          # insert it into the collection
        return data




