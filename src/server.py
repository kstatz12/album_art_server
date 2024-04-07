"""api for spotify app."""

import threading
import spotipy
from spotipy import oauth2
from bottle import route, run, request, response
from img import get_album_art
from upload import upload_to_dropbox

SCOPE = "user-read-currently-playing"
sp_auth = oauth2.SpotifyOAuth(scope=SCOPE)

cacheUrl = ""

timer = threading.Timer(30.0, lambda: upload())

def upload():
    """Upload image to dropbox."""
    token = __authGuard()
    if not token:
        return
    sp = spotipy.Spotify(auth=token)
    url = get_album_art_url(sp.currently_playing())
    if url == None:
        return
    if url == cacheUrl:
        return
    cacheUrl = url
    data = get_album_art(sp.currently_playing())
    upload_to_dropbox(data)

def get_album_art_url(response):
    """Return album art url from response."""
    if(response == None):
        return None
    return response['item']['album']['images'][0]['url']

@route('/')
def index():
    """Return image png data or login form."""
    try:
        token = __authGuard()
        if token:
            timer.start()
            return "logged In"
        else:
            auth_url = sp_auth.get_authorize_url()
            return "<a href='%s'>Login</a>" % auth_url
    except Exception as e:
        print(e)
        return "Error"

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

run(host='', port=8080)
