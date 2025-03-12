from Cupidv3Backend.settings import CLIENT_SECRET
from CupidV3Database.matchingdb import Profile

from fastapi import FastAPI, Response, Cookie, Request  
from typing import Optional
from starlette.responses import RedirectResponse
from aiohttp import ClientSession, BasicAuth
from pydantic import BaseModel
from discord.utils import setup_logging
from uuid import uuid4

import uvicorn
import redis
import json

# classes
class BaseProfile(BaseModel):
    user_id:int|str
    name:str
    age: int|str
    age_specified:str|None
    pronouns:str
    gender:str
    gender_specified:str
    sexuality:str
    bio:str

setup_logging()
# constants 
API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1343727517529542718'
REDIRECT_URI = 'http://localhost:5173/api/0auth/exchange'

# global functions
async def exchange_code(code:str):
    """exchanges a discord 0auth code for a barrer token

    Args:
        code (str): the code to exchange witth

    Returns:
        dict: the json data of of the post requests
    """
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    async with ClientSession() as session:
        response = await session.post(f"{API_ENDPOINT}/oauth2/token", data=data,headers=headers, auth=BasicAuth(CLIENT_ID, CLIENT_SECRET))
        return await response.json()


async def cache_user_data(exchange_data:dict) -> str:
    """caches user data in redis given discord 0auth token info

    Args:
        exchange_data (dict): _description_

    Returns:
        str: the session id of the reddis session
    """
    # get the user profile
    token_type = exchange_data.get('token_type')
    access_token = exchange_data.get('access_token')
    expires_in = exchange_data.get('expires_in')
    session_id = str(uuid4())
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'{token_type} {access_token}'
    }

    async with ClientSession() as session:
        response = await session.get(f"{API_ENDPOINT}/users/@me", headers=headers)
        response_json = await response.json()
    
    session_data = response_json
    session_data["access_token"] = access_token
    seralized_session_data = json.dumps(session_data)
    redis_client.setex(session_id, expires_in, seralized_session_data)

    return session_id
    

# varibles
app = FastAPI(debug=True)
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)


# routes
@app.get('/api/0auth/exchange')
async def api_0auth_exchange(code:str):
    """takes the discord exchange code, creates a session, and stores it.

    Args:
        code (str): the 0auth exchange code

    Returns:
        RedirectResponse: the redirect response, ether discord 0auth on failure, or root on success
    """
    exchange_data:dict = await exchange_code(code)

    if exchange_data.get("error"):
        response = RedirectResponse(url="https://discord.com/oauth2/authorize?client_id=1343727517529542718&response_type=code&redirect_uri=http%3A%2F%2Flocalhost%3A5173%2Fapi%2F0auth%2Fexchange&scope=identify+guilds+email")
        return response
    
    session_id = await cache_user_data(exchange_data)
    response = RedirectResponse(url='/')
    response.set_cookie("session_id", session_id)
    
    return response

@app.get('/api/0auth/profile')
async def apu_0auth_profile(request:Request, session_id: Optional[str] = Cookie(None)):
    try:
        if session_id:
            data = json.loads(redis_client.get(session_id))
            return {'success':True, 'profile':data}
        else:
            return {'success':False, 'message':'User is not logged in!'}
    except:
        return {'success':False, 'message':'Some error occured, user may not be logged in'}

@app.get('/api/0auth/clear')
async def apu_0auth_clear():
    """Logs the user out and clears their session

    Returns:
        RedirectResponse: a redirect that sets the cookie
    """
    redis_client.setex()
    response = RedirectResponse('/')
    response.set_cookie('session_id', None, expires=1)
    return response


@app.get('/api/profiles/get/{user_id}')
async def api_profiles_get_id(user_id:int):
    """Gets a profile with a provided_id

    Args:
        user_id (int): the if of the users profile to get

    Returns:
        dict: the profile if found
    """
    profile, _ = await Profile.get_profile(user_id)
    if profile:
        matching_profile = json.dumps(profile.__dict__)
        return {'success':True, 'matching_profile':matching_profile}
    else: return {'success':False}

@app.get('/api/profiles/delete/{user_id}')
async def api_profiles_delete(user_id:int, session_id: Optional[str] = Cookie(None)):
    try:
        if session_id:
            data:dict = json.loads(redis_client.get(session_id))
            if int(data.get('id')) != user_id:
                print(data)
                print(data.get('id'))
                print(user_id)
                return {'success':False, 'message':'Can\'t delete a profile thats not your own!'}
            await Profile.delete_profile(int(data.get('id')))
            return {'success':True, 'message':'Profile Successfully deleted'}
        else:
            return {'success':False, 'message':'User is not logged in!'}
    except Exception as e:
        return {'success':False, 'message':f'{e}'}


@app.post('/api/profiles/update/{user_id}')
async def api_profiles_update(user_id:int, base_profile:BaseProfile, request:Request):
    """Using a base profile model, updates a mongodb PROFILE

    Args:
        user_id (int): the id of the user
        base_profile (BaseProfile): base profile, already passed by the requests
        request (Request): _description_

    Returns:
        dict: weather the update was successful or not
    """
    try:
        profile, created = await Profile.get_profile(
            user_id,
            True,
            name=base_profile.name,
            age=base_profile.age,
            pronouns=base_profile.pronouns,
            gender=base_profile.gender,
            sexuality=base_profile.sexuality,
            bio=base_profile.bio)
        
        if created: 
            await profile.update({"$set": {
                "name":base_profile.name,
                "age":base_profile.age,
                "pronouns":base_profile.pronouns,
                "gender":base_profile.gender,
                "sexuality":base_profile.sexuality,
                "bio":base_profile.bio,
            }})
        
        packet = {'event':"profile_update", "profile_id":profile.user_id}
        seralized_packet = json.dumps(packet)

        redis_client.publish("bot_channel", seralized_packet)

        return {'success':True}
        
    except Exception as error:
        return {'success':False, 'message':error}

    

def main():
    uvicorn.run(app, port=5000)

if __name__ == "__main__":
    main()