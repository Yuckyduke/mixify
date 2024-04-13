from app import app
from flask import render_template, request, url_for, redirect, session
from app import spotify
import base64
import requests


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
        print("poop")
    token_data = mySpot.getAccessToken(auth_code)
    accessToken = token_data.get("access_token")
    session['access_token'] = accessToken
    return redirect(url_for("webplayer"))

@app.route('/webplayer')
def webplayer():
    # use the access token to activate the webplayer
    access_token = session.get('access_token')
    if not access_token:
        print("yo")
        redirect(url_for('index'))
    data = mySpot.playlists(access_token)
    print(data)
    return render_template("webplayer.html", access_token = access_token, data = data) 

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()  # Assumes data is sent as JSON
    
    # Process the data (you can do more meaningful processing here)
    #result = {'status': 'success', 'message': 'Data received successfully', 'processed_data': data}
    #print(data["playlist"])
    #return mySpot.getPlaylistSongs(se(ssion.get("access_token"), result["processed_data"])
    #mySpot.clearQueue(session.get("access_token"))
    #mySpot.queuePlaylist(session.get("access_token"), playlist)
    return mySpot.getPlaylistSongs(session.get("access_token"), data["playlist"]) 

@app.route('/getSongDuration', methods=['POST'])
def getSongDuration():
    data = request.get_json()
    print(data)
    print(mySpot.uriToID(data))
    test = mySpot.getSongDuration(access_token=session.get("access_token"), songURI=data)
    print(test)
    return test
