from flask import Flask, request, session, redirect, jsonify
import requests

from Cupidv3Backend.settings import CLIENT_SECRET
from CupidV3Database.matchingdb import Profile

app = Flask(__name__)
app.secret_key = 'ahasujhfa'



API_ENDPOINT = 'https://discord.com/api/v10'
CLIENT_ID = '1343727517529542718'
REDIRECT_URI = 'http://localhost:5173/api/auth'

def exchange_code(code):
  data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': REDIRECT_URI
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post('%s/oauth2/token' % API_ENDPOINT, data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
  return r.json()




@app.route('/')
async def test():
    return 'hi'

@app.route('/api/auth')
async def api_auth():
    code = request.args.get('code')
    token_data = exchange_code(code)
    session['token_data'] = token_data
    return redirect('/')

@app.route('/api/get/access')
async def api_get_access():
    state = False
    message = ''
    token_data = session.get('token_data')
    if token_data: state = True
    else: message = 'failed to get token data'

    return jsonify({'success':state, 'message':message, 'token_data':token_data})



@app.route('/api/update/profile', methods=['POST'])
async def api_update_profile():
    data:dict = request.get_json()
    user_id = int(data.get('user_id'))
    name = data.get('name')
    age = data.get('age')
    pronouns = data.get('pronouns')
    gender = data.get('gender')
    sexuality = data.get('sexuality')
    bio = data.get('bio')

    profile = await Profile.get_profile(user_id)
    if profile:
        # update
        pass
    else:
        # create
        profile = await Profile.create_profile(user_id,name,age,pronouns,gender,sexuality,bio)

    return jsonify({'success':True})



@app.route('/api/logout')
async def api_logout():
    session['token_data'] = None
    return redirect('/')

#app.run(debug=True)