from flask import Flask, request, session, redirect
import requests
from settings import CLIENT_SECRET

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


app.run(debug=True)