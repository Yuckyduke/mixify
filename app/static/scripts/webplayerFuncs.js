// MARK: Global
let Player;
function timeConverter(msTime) {
  seconds = Math.floor((msTime % 60000)/1000);
  minutes = Math.floor(msTime/60000);
  if (seconds < 10) {
    return minutes.toString() + ":0" + seconds.toString();
  } else {
    return minutes.toString() + ":" + seconds.toString();
  }
}

function addASecond() {
  trackPosition = trackPosition + 1000
  document.getElementById("current-time").textContent = !isNaN(trackPosition) 
  ? timeConverter(trackPosition) : "00:00";
  document.getElementById("songSeek").value = (trackPosition/trackDuration) * 100;
  console.log(trackPosition);
}

// MARK: Main Run Loop
function handleSpotify(player) {
  Player = player;
  let currentTrack;
  let secondCounter;
  // Ready
  player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id);
  });

  // Not Ready
  player.addListener('not_ready', ({ device_id }) => {
    console.log('Device ID has gone offline', device_id);
  });

  player.addListener('initialization_error', ({ message }) => {
    console.error(message);
  });

  player.addListener('authentication_error', ({ message }) => {
    console.error(message);
  });

  player.addListener('account_error', ({ message }) => {
    console.error(message);
  });
  //TODO Add seek to here
  document.getElementById("songSeek").onchange = function () {
    value = document.getElementById("songSeek").value;
    player.seek((value/100) * trackDuration);
  }
  document.getElementById('nextSong').onclick = function () {
    player.nextTrack();
    clearInterval(secondCounter);
    secondCounter = setInterval(addASecond, 1000);
  };
  document.getElementById('togglePlay').onclick = function () {
    player.togglePlay();
    IsPaused ? IsPaused = false : IsPaused = true;
    if (IsPaused) {
      IsPaused = false;
      clearInterval(secondCounter);
    } else {
      IsPaused = true;
      secondCounter = setInterval(addASecond, 1000);
    }
  };
  document.getElementById('lastSong').onclick = function () {
    player.previousTrack();
  };
  player.addListener('player_state_changed', ({
    position,
    duration,
    paused,
  track_window: { current_track }
  }) => {
    IsPaused = paused;
    if (!IsPaused) {
      clearInterval(secondCounter);
      secondCounter = setInterval(addASecond, 1000);
    }
    trackPosition = position;
    trackDuration = duration;
    document.getElementById("songName").textContent = current_track.name;
    document.getElementById("songArt").src = current_track.album.images[0].url;
    document.getElementById("total-duration").textContent = timeConverter(duration);
    document.getElementById("current-time").textContent = timeConverter(trackPosition);
    currentTrack = current_track;
    currentTrackURI = current_track.uri;
    highlightTrack(current_track.name, current_track.artists[0]["name"]);
  });
  player.connect();
}

// TODO: Add ability to start and stop song based off user selected times.
// Have access to Player globally.
function startSong() {
  console.log("Song started.");
  // Start playing the song here
}

// Function to stop the song
function stopSong() {
  console.log("Song stopped.");
  // Stop playing the song here
}

// Function to handle song duration
function playSongWithDuration(duration) {
  // Start the song
  startSong();

  // Stop the song after the specified duration
  setTimeout(stopSong, duration);
}

// Example: Play the song for 5 seconds
playSongWithDuration(5000); // 5000 milliseconds = 5 seconds
