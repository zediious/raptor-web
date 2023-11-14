console.log("raptormc.js loaded")

function closeOffCanvas() {

  let closeCanvas = document.querySelector('[data-bs-dismiss="offcanvas"]');
  closeCanvas.click();

}

function closeModal() {

  $('.modal').modal('hide');
  console.log("did run closeModal")

}

document.getElementById("body").onscroll = function myFunction() {  
    var scrolltotop = document.scrollingElement.scrollTop;
    var target = document.getElementById("backgroundWrapper");
    var xvalue = "center";
    var factor = 0.5;
    var yvalue = scrolltotop * factor;
    target.style.backgroundPosition = xvalue + " " + yvalue + "px";
  }
  