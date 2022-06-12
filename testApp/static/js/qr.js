let reservation = false
$( document ).ready( () => {
  $("#restart-camera").click(() => {

    $("#restart-camera").attr('hidden', 'hidden');
    cameraOnline()
  })
  $("#scan-click").click( () => {
    $("#scan-click").css("display","none")
    $("#loading").removeClass("d-none")
    $("#preview").removeAttr("hidden")
    cameraOnline()
  })
  $.ajax({
    url : "/",
    type: "POST",
    data : {
        csrfmiddlewaretoken : getCookie("csrftoken")
    },
    success: function(data, textStatus, jqXHR)
    {
        if(data.status != "ok")
          $("#scan-click").removeAttr("hidden")
        else
        {
          reservation = true
          $("#map").removeAttr("hidden")
          $(".finish-ride").removeAttr("hidden")
        }

    },
    error: function (jqXHR, textStatus, errorThrown)
    {
        console.log("Path is not available")
        $("#scan-click").removeAttr("hidden")
    }
});
})
cameraOnline = () => {
  let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
  scanner.addListener('scan', function (content) {
    console.log(content);
    console.log(getCookie("csrftoken"))
    url = "/start-trip/"
    $.post(url,
      {
        bike_code : content,
        csrfmiddlewaretoken : getCookie("csrftoken")
      }).then((res) => {
        if(res.status === "error")
        {
          console.log("Edge case, wrong QR")
          $("#notification").toast('show');
        }
        else
        {
          reservation = true
          scanner.stop()
          $("#preview").hide()
          $("#restart-camera").removeAttr('hidden');

          $("#map").removeAttr('hidden')
          $(".finish-ride").removeAttr("hidden")
        }
      })
      .catch((error) => {
        location.href = 'login';
      })
  });
  Instascan.Camera.getCameras().then(function (cameras) {
    if (cameras.length > 2) {
      scanner.start(cameras[2]).then(() => {
        $("#text-camera").hide()
        $("#loading").addClass("d-none")
      });
    } 
    else if (cameras.length == 1)
    {
      scanner.start(cameras[0]).then(() => {
        $("#text-camera").hide()
        $("#loading").addClass("d-none")
      });
    } 
    else 
      console.error('No cameras found.');
    
  }).catch(function (e) {
    console.error(e);
  });
}