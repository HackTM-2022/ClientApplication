let lastPoints = []
let loopEvery5Seconds = null;
let map;
window.initMap = initMap;

function GetLatestData()  {
    $.ajax({
        url : "/",
        type: "POST",
        data : {
            csrfmiddlewaretoken : getCookie("csrftoken")
        },
        success: function(data, textStatus, jqXHR)
        {
            lastPoints = []
            let i = 0
            data.forEach((elem) => {
                lastPoints.push({lat: i/4, lng : i/4})
                i++
            })
            let flightPath = new google.maps.Polyline({
                path: lastPoints,
                geodesic: true,
                strokeColor: "#FF0000",
                strokeOpacity: 1.0,
                strokeWeight: 2,
              });
              flightPath.setMap(map);
        },
        error: function (jqXHR, textStatus, errorThrown)
        {
            console.log("Path is not available")
        }
    });
}



function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 45.760696, lng: 21.226788 },
    zoom: 10,
  });
  map.addListener('tilesloaded', () => {
    if(loopEvery5Seconds == null)
        loopEvery5Seconds = window.setInterval( () => {
            GetLatestData()
        }, 5000);
      
  })
}

