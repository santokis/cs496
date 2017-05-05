import json
import flask
import requests

app = flask.Flask(__name__)

CLIENT_ID = '591609081019-91ofhlko8vmuq1us1cu3tgbdsao761mv.apps.googleusercontent.com'
CLIENT_SECRET = '3PdjI0tfRg74a3uBdSpB6_LZ'  # Read from a file or environmental variable in a real app
SCOPE = 'https://www.googleapis.com/auth/plus.metadata.readonly'
REDIRECT_URI = 'https://assignment4-166505.appspot.com/oauth'

@app.route('/')
def index():
  if 'credentials' not in flask.session:
    return flask.redirect(flask.url_for('oauth2callback'))
  credentials = json.loads(flask.session['credentials'])
  if credentials['expires_in'] <= 0:
    return flask.redirect(flask.url_for('oauth2callback'))
  else:
    headers = {'Authorization': 'Bearer {}'.format(credentials['access_token'])}
    req_uri = 'https://www.googleapis.com/drive/v2/files'
    r = requests.get(req_uri, headers=headers)
    return r.text


@app.route('/oauth2callback')
def oauth2callback():
  if 'code' not in flask.request.args:
    auth_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code'
                '&client_id={}&redirect_uri={}&scope={}').format(CLIENT_ID, REDIRECT_URI, SCOPE)
    return flask.redirect(auth_uri)
  else:
    auth_code = flask.request.args.get('code')
    data = {'code': auth_code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'}
    r = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
    flask.session['credentials'] = r.text
    return flask.redirect(flask.url_for('index'))


if __name__ == '__main__':
  import uuid
  app.secret_key = str(uuid.uuid4())
  app.debug = False
  app.run()