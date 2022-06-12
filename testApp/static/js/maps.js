let lastPoints = []
let loopEvery5Seconds = null;
let map;
window.initMap = initMap;
$(document).ready(() => {
    if(reservation == true)
        GetLatestData()
    $(".finish-ride").click(() => {
        console.log("DA")
        $.post("/end-trip/", {
            csrfmiddlewaretoken : getCookie("csrftoken")
        }).then(() => {
            location.reload();
        })
    })
})
function GetLatestData()  {
    $.ajax({
        url : "/",
        type: "POST",
        data : {
            csrfmiddlewaretoken : getCookie("csrftoken")
        },
        success: function(data, textStatus, jqXHR)
        {
            if(data.status == "ok")
            {
                lastPoints = []
                let i = 0
                data.f_Data.forEach((elem) => {
                    lastPoints.push({lat: parseFloat(elem.lat), lng : parseFloat(elem.lon)})
                    i++
                })
                console.log(lastPoints)
                let flightPath = new google.maps.Polyline({
                    path: lastPoints,
                    geodesic: true,
                    strokeColor: "#FF0000",
                    strokeOpacity: 1.0,
                    strokeWeight: 2,
                  });
                  flightPath.setMap(map);
            }
            else {
                location.reload()
            }

        },
        error: function (jqXHR, textStatus, errorThrown)
        {
            console.log("Path is not available")
            location.reload()
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
            if(reservation == true)
                GetLatestData()
        }, 5000);
      
  })
}

