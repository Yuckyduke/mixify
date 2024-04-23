import requests
from flask import redirect, jsonify
from urllib.parse import urlencode
import base64

class spotifyHandler:

    def __init__(self, clientID: str) -> None:
        #initialize a spotify handler with the required credentials
        """
        Initialze a spotify handler with the required credentials

        Scope: Gives permissions for api to do certain things
        Redirect_URI: Will handle callback from spotify
        SpotURl: the start of login endpoint
        Params: Dictionary for redirect_URL, SpotURL, and params
        Secret: Secret key to exchange for access Token
        spotify Token URL: Start point for api endpoints
        """
        self.clientID = clientID
        self._scope = "user-read-private user-read-email streaming playlist-read-private playlist-read-collaborative user-read-currently-playing user-modify-playback-state"
        self.redirect_uri = "http://127.0.0.1:5000/callback"
        self.spot_url = "https://accounts.spotify.com/"
        self.params = {"client_id": self.clientID, "response_type": "code", "redirect_uri" :self.redirect_uri, "scope": self._scope}
        self.secret = 
        self.spotifyTokenURL = 'https://accounts.spotify.com/api/token'

    def authenticate(self) -> redirect:
        """
        The authorize URL will send a callback to the self.redirect_url

        See routes.py for how this is handled 
        """
        authorizeUrl = self.spot_url + "authorize"
        return redirect(f'{authorizeUrl}?{urlencode(self.params)}')
    
    def getAccessToken(self, auth_code) -> requests.Response:
    # Exchange authorization code for access token
        headers = {
            'Authorization': f'Basic {base64.b64encode(f"{self.clientID}:{self.secret}".encode()).decode()}',
        }
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
        }
        try:
            response = requests.post(self.spotifyTokenURL, headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)

    def playlists(self, access_token) -> dict:
        """
        Call playlist endpoint to retreive users playlist 
    
        Returns a playlistName: playlistID dictionary
        """
        try:
            response = requests.get("https://api.spotify.com/v1/me/playlists", headers= {"Authorization": "Bearer " + access_token})
            if response.status_code == requests.codes.ok:
                items = response.json()['items']
                playlistDict = {}
                for item in items:
                    playlistDict[item['name']] = item['id']
                return playlistDict
            else:
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error", e)
            return {}
    
    def playPlaylist(self, playlistID, access_token):
        """
        Calls the player play endpoint PUT
        Used with the get Playlists songs to also play the playlist
        """
        apiUrl = "https://api.spotify.com/v1/me/player/play" 
        headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
        }
        data = {
            "context_uri": f"spotify:playlist:{playlistID}",
            "position_ms": 0
        }
        try:
            response = requests.put(url=apiUrl, headers= headers, json=data)
            if response.status_code == requests.codes.ok:
                print("PUT request was succesfull")
            else:
                response.raise_for_status()
        #return response
        except requests.exceptions.RequestException as e:
            print("Error:", e)
    
    def getPlaylistSongs(self, access_token, playlist_id):
        """
        Get the songs of a playlist - get request with playlist id

        If the playlist is obtained it will send a put request to play the playlist 
        """
        response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}", headers ={"Authorization": "Bearer " + access_token}).json()
        returnArray = []
        try:
            responseItems = response["tracks"]["items"]
        except:
            print("Unable to obtain playlist")
            return
        for i in range(len(response["tracks"]["items"])):
            currentTrack = {"row": i, "name": responseItems[i]["track"]["name"], 
                            "id": responseItems[i]["track"]["uri"], "artists": responseItems[i]["track"]["artists"][0]["name"], 
                            "duration": responseItems[i]["track"]["duration_ms"]}
            #self.addSongToQueue(responseItems[i]["track"]["uri"], access_token)
            returnArray.append(currentTrack)
        self.playPlaylist(playlist_id, access_token)
        return jsonify({"tracks": returnArray})
    

    def addSongToQueue(self, song_uri, access_token):
        """
        OLD function DONT USE
        """
        add_to_queue_url = f'https://api.spotify.com/v1/me/player/queue?uri={song_uri}'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(url=add_to_queue_url, headers=headers)
        if response.status_code == 202:
            print("Song added to the queue successfully.")
        else:
            print(f"Failed to add song to the queue. Status code: {response.status_code}") 

    def getQueue(self, access_token):
        """
        OLD function DONT USE
        """
        response = requests.get("https://api.spotify.com/v1/me/player/queue", headers ={"Authorization": "Bearer " + access_token}).json()
        return response

    def getSongDuration(self, songURI, access_token):
        """
        OLD FUNCTION DONT USE
        """
        songID = self.uriToID(songURI)
        response = requests.get(f"https://api.spotify.com/v1/tracks/{songID}", headers ={"Authorization": "Bearer " + access_token}).json()
        return str(response["duration_ms"])

    def uriToID(self, songURI):
        """
        OLD Function don't use
        """
        test = songURI[songURI.find(":") + 1:]
        test = test[test.find(":") + 1:]
        return test

    def clearQueue(self, access_token):
        """
        OLD function don't use
        """
        while self.getQueue(access_token):
            requests.post(url = "https://api.spotify.com/v1/me/player/next", headers = {"Authorization": "Bearer " + access_token})


     
