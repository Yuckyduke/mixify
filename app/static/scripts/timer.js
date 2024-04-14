if (songStart | unPaused) {
let timeoutID = setTimeout(() => {
    nextSong();
  }, end - currentPosition);
}
if (playbackState = "paused" & timeoutID){
    clearTimeout(timeoutID);
}