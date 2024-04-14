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
    const currentPlaylist = { "playlist": playlists[document.getElementById("playlistDropdown").value] };
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
            if (i == 0){
              playlistDict["start"] = 0
            }
            else{
              playlistDict["stop"] = 0;
            }
            const cell = row.insertCell();
            cell.textContent = 0;
            cell.setAttribute('contenteditable', 'true');
          }
        });

        // Append the table to the body of the document
        document.body.appendChild(table);
      })
  }