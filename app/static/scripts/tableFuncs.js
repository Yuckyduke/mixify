function highlightTrack(song, artist) {
    table = document.getElementById("Playlist");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
      songName = tr[i].getElementsByTagName("td")[1]
      artistName = tr[i].getElementsByTagName("td")[2]
      if (songName && artistName) {
        songTxtValue = songName.textContent || songName.innerText;
        artistTxtValue = artistName.textContent || artistName.textContent
        if (songTxtValue == song && artistTxtValue == artist) {
          tr[i].style.backgroundColor = "orange";
        } else {
          tr[i].style.backgroundColor = ""
        }
      }
    }
  }

function getStartStop(song, artist){
  table = document.getElementById("Playlist");
  tr = table.getElementsByTagName("tr");

  for (i=0; i<tr.length; i++) {
    songName = tr[i].getElementsByTagName("td")[1];
    artistName = tr[i].getElementsByTagName("td")[2];
    if (songName && artistName) {
      songTxtValue = songName.textContent || songName.innerText;
      artistTxtValue = artistName.textContent || artistName.textContent
      if (songTxtValue == song && artistTxtValue == artist) {
        console.log([parseInt(tr[i].getElementsByTagName("td")[5].innerText), parseInt(tr[i].getElementsByTagName("td")[6].innerText)]);
        return;
      }
    }
  }
}

  function updatePlaylist() {
    const currentPlaylistName = document.getElementById("playlistDropdown").value
    const currentPlaylist = { "playlist": playlists[currentPlaylistName] };
    const globalCache = loadDictionary();
    fetch('/process_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(currentPlaylist)
    })
      .then(response => response.json())
      .then(result => {
        let playlistDict = result;
        const table = document.getElementById('Playlist');
        const rowCount = table.rows.length;

        // Start from the bottom to avoid index issues as rows are removed
        for (let i = rowCount - 1; i > 0; i--) {
          table.deleteRow(i);
        }

        // Create rows and cells for the data
        result.tracks.forEach(item => {
          const row = document.getElementById("Playlist").insertRow();
          let cell = row.insertCell();
          cell.textContent = item["row"];
          cell = row.insertCell();
          cell.textContent = item["name"];
          cell = row.insertCell();
          cell.textContent = item["artists"];
          cell = row.insertCell();
          cell.textContent = item["id"];
          cell = row.insertCell();
          cell.textContent = item["duration"];
          for (let i = 0; i < 2; i++) {
            const cell = row.insertCell();
            if (i == 0) {
              if(isCacheValid()) {
                cell.textContent = globalCache[currentPlaylistName][item["id"]][1];
              } else {
                cell.textContent = 0;
              }
              playlistDict["start"] = 0
            } else {
              if (isCacheValid()) {
                cell.textContent = globalCache[currentPlaylistName][item["id"]][2];
              } else {
                cell.textContent = 0;
              }
              playlistDict["stop"] = 0;
            }
            cell.setAttribute('contenteditable', 'true');
          }
        });

        // Append the table to the body of the document
        document.body.appendChild(table);
      })
  }

  function isCacheValid() {
    const currentPlaylistName = document.getElementById("playlistDropdown").value
    const globalCache = loadDictionary()
    return ((typeof(globalCache) != 'undefined') && 
    (typeof(globalCache[currentPlaylistName]) != 'undefined'))
  }

  function updateCache(changes) {
    var globalCache = loadDictionary();
    if (typeof(globalCache) === 'undefined') {
      globalCache = {};
    }
    globalCache[document.getElementById("playlistDropdown").value] = changes;
    window.localStorage.setItem("storedDict", JSON.stringify(globalCache));
    console.log(globalCache);
  }

  function loadDictionary() {
    return JSON.parse(window.localStorage.getItem("storedDict"));
  }

  function hashPlaylist() {
    table = document.getElementById("Playlist");
    tr = table.getElementsByTagName("tr");
    var dict = {};
    for (i=1; i<tr.length; i++) {
      row = tr[i].getElementsByTagName("td");
      uri = row[3].innerText;
      duration = parseInt(row[4].innerText);
      start = parseInt(row[5].innerText);
      end = parseInt(row[6].innerText);
      if (start <= duration & end <= duration & start <= end & start >= 0 & end >= 0){
        dict[uri] = [duration, start, end];
      }
      else {
        alert("Invalid start and stops");
        return;
      }
    }
    updateCache(dict);
    return dict
}