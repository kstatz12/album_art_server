"""api for spotify app."""
import spotipy
from spotipy import oauth2
from bottle import route, run, request

SCOPE = "user-read-currently-playing"

sp_auth = oauth2.SpotifyOAuth(scope=SCOPE)

@route('/')
def index():
    """Return OK or login form."""
    token = __authGuard()
    if token:
        return "OK"
    else:
        return "<a href='/login'>Login</a>"

@route('/login')
def login():
    """Login to spotify."""
    if __authGuard():
        return "Already logged in"
    else:
        auth_url = sp_auth.get_authorize_url()
        return "<a href='%s'>Login</a>" % auth_url

@route('/current')
def current():
    """Return current song."""
    token = __authGuard()
    if token:
        sp = spotipy.Spotify(auth=token)
        return sp.current_user_playing_track()
    else:
        return "<a href='/login'>Login</a>"

def __authGuard():
    """Auth guard."""
    access_token = ""
    token_info = sp_auth.get_cached_token()
    if token_info:
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_auth.parse_response_code(url)
        if code != url:
            token_info = sp_auth.get_access_token(code)
            access_token = token_info['access_token']

        if access_token:
            return access_token
        else:
            return None

run(host='localhost', port=8080)
