  function timeConverter(msTime){
    seconds = Math.floor((msTime % 60000)/1000);
    minutes = Math.floor(msTime/60000);
    if (seconds < 10){
      return minutes.toString() + ":0" + seconds.toString();}
    else{
    return minutes.toString() + ":" + seconds.toString();}
  }
  function addASecond(){
    trackPosition = trackPosition + 1000
    document.getElementById("current-time").textContent = !isNaN(trackPosition) 
    ? timeConverter(trackPosition) : "00:00";
    document.getElementById("songSeek").value = (trackPosition/trackDuration) * 100;
    console.log(trackPosition);
  }