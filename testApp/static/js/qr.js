$( document ).ready( () => {
  cameraOnline()
  $("#restart-camera").click(() => {

    $("#restart-camera").attr('hidden', 'hidden');
    cameraOnline()
  })
})

cameraOnline = () => {
  let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
  scanner.addListener('scan', function (content) {
    console.log(content);
    console.log(getCookie("csrftoken"))
    content = "/start-trip/"
    $.post(content,
      {
        bike_code : "2a421ad4-224e-4c7f-b64f-8d46df20ecad",
        csrfmiddlewaretoken : getCookie("csrftoken")
      }).then((res) => {
        console.log(res)
        if(res.status === "error")
        {
          scanner.stop()
          $("#text-camera").text("There was an error getting your bike!").show()
          $("#preview").hide()
          $("#restart-camera").removeAttr('hidden');
        }
        else
        {

        }
      })
  });
  Instascan.Camera.getCameras().then(function (cameras) {
    if (cameras.length > 0) {
      scanner.start(cameras[0]).then(() => {
        $("#text-camera").hide()
      });

    } else {
      console.error('No cameras found.');
    }
  }).catch(function (e) {
    console.error(e);
  });
}