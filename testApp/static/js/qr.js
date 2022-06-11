$( document ).ready( () => {
  let scanner = new Instascan.Scanner({ video: document.getElementById('preview') });
  scanner.addListener('scan', function (content) {
    console.log(content);
    console.log(getCookie("csrftoken"))
    content = "/start-trip"
    $.post(content,
      {
        bike_code : 11234344354544,
        csrfmiddlewaretoken : getCookie("csrftoken")
      })
  });
  Instascan.Camera.getCameras().then(function (cameras) {
    if (cameras.length > 0) {
      scanner.start(cameras[0]);
    } else {
      console.error('No cameras found.');
    }
  }).catch(function (e) {
    console.error(e);
  });
})

