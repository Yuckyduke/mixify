from app import app
from flask import render_template, request, url_for, redirect, session
from app import spotify

#handler instance
mySpot = spotify.spotifyHandler("01f4d277eb0a45a9a5fbd08cce6a6afe")
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'

@app.route('/')
def index():
    return mySpot.authenticate()

@app.route('/login')
def login():
    return mySpot.authenticate()

@app.route('/callback/')
def callback():
    # Handle the callback from Spotify
    auth_code = request.args.get("code")
    if auth_code is None:
    # TODO: Handle error
        return redirect(url_for("error"))
    token_data = mySpot.getAccessToken(auth_code)
    accessToken = token_data.get("access_token")
    #hash our access token so that we can use later
    session['access_token'] = accessToken
    return redirect(url_for("webplayer"))

@app.route('/webplayer')
def webplayer():
    # use the access token to activate the webplayer
    access_token = session.get('access_token')
    if not access_token:
        # TODO: Log this error?
        print("Access code was not obtained")
        return redirect(url_for('error'))
    data = mySpot.playlists(access_token)
    return render_template("webplayer.html", access_token = access_token, data = data) 

@app.route('/process_data', methods=['POST'])
def process_data():
  # TODO: Wrap this in a try:except:
    try:
        data = request.get_json()  # Assumes data is sent as JSON
        return mySpot.getPlaylistSongs(session.get("access_token"), data["playlist"])
    except:
        return redirect(url_for("error"))

@app.route('/error')
def error():
    """
    Error page if authorize does not work
    """
    return "Authorization Code was not Obtatined"

@app.route('/getSongDuration', methods=['POST'])
def getSongDuration():
    data = request.get_json()
    print(data)
    print(mySpot.uriToID(data))
    test = mySpot.getSongDuration(access_token=session.get("access_token"), songURI=data)
    print(test)
    return test
