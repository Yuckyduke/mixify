import requests
from flask import redirect, request, jsonify
from urllib.parse import urlencode
import base64

class spotifyHandler:

    def __init__(self, clientID: str) -> None:
        #initialize a spotify handler with the required credentials
        self.clientID = clientID
        self._scope = "user-read-private user-read-email streaming playlist-read-private playlist-read-collaborative user-read-currently-playing user-modify-playback-state"
        self.redirect_uri = "http://127.0.0.1:5000/callback"
        self.spot_url = "https://accounts.spotify.com/"
        self.params = {"client_id": self.clientID, "response_type": "code", "redirect_uri" :self.redirect_uri, "scope": self._scope}
        self.secret = "bd5fb29c425c4d108f34f44a78bebb52"
        self.spotifyTokenURL = 'https://accounts.spotify.com/api/token'

    def getCode(self) -> str:
        try:
            response = requests.get(url = self.spot_url + 'login',params= {"client_id":self.clientID, "response_type":"code", "redirect_uri": self.redirect_uri, "scope": self._scope})
            if response.status_code == requests.codes.ok:
                self.code = response
                return self.code
        except requests.exceptions.RequestException as e:
            print("Error:", e)

 
    def authenticate(self) -> None:
        authorizeUrl = self.spot_url + "authorize"
        return redirect(f'{authorizeUrl}?{urlencode(self.params)}')
    
    def getAccessToken(self, auth_code):
    # Exchange authorization code for access token
        headers = {
            'Authorization': f'Basic {base64.b64encode(f"{self.clientID}:{self.secret}".encode()).decode()}',
        }
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': self.redirect_uri,
        }
        response = requests.post(self.spotifyTokenURL, headers=headers, data=data)
        return response.json()

    def playlists(self, access_token):
    # return playlist names and ids
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
        #play a playlist
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
        # return the songs of a playlist
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
        print(playlist_id)
        self.playPlaylist(playlist_id, access_token)
        return jsonify({"tracks": returnArray})
    

    def addSongToQueue(self, song_uri, access_token):
    # Add the song to the queue
        add_to_queue_url = f'https://api.spotify.com/v1/me/player/queue?uri={song_uri}'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.post(url=add_to_queue_url, headers=headers)
        if response.status_code == 202:
            print("Song added to the queue successfully.")
        else:
            print(f"Failed to add song to the queue. Status code: {response.status_code}") 

    def getQueue(self, access_token):
        #return the queue
        response = requests.get("https://api.spotify.com/v1/me/player/queue", headers ={"Authorization": "Bearer " + access_token}).json()
        return response

    def getSongDuration(self, songURI, access_token):
        songID = self.uriToID(songURI)
        response = requests.get(f"https://api.spotify.com/v1/tracks/{songID}", headers ={"Authorization": "Bearer " + access_token}).json()
        return str(response["duration_ms"])

    def uriToID(self, songURI):
        test = songURI[songURI.find(":") + 1:]
        test = test[test.find(":") + 1:]
        return test

    def clearQueue(self, access_token):
        #clear the current queue
        while self.getQueue(access_token):
            requests.post(url = "https://api.spotify.com/v1/me/player/next", headers = {"Authorization": "Bearer " + access_token})


     
