console.log("raptormc.js loaded")

window.onload = function() {

  if (localStorage.getItem('serverbox_expanded') == "no") {
    $("#serverBoxCollapse").toggleClass("show");
  }

}

function setExpandedState() {

  if (localStorage.getItem('serverbox_expanded') == "yes") {
    localStorage.setItem('serverbox_expanded','no')
  }

  else {
    localStorage.setItem('serverbox_expanded','yes')
  }

}

document.getElementById("body").onscroll = function myFunction() {  
    var scrolltotop = document.scrollingElement.scrollTop;
    var target = document.getElementById("backgroundWrapper");
    var xvalue = "center";
    var factor = 0.5;
    var yvalue = scrolltotop * factor;
    target.style.backgroundPosition = xvalue + " " + yvalue + "px";
  }