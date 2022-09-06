console.log("raptormc.js loaded")

$( document ).ready(function() {
  new ClipboardJS('.copyNomiAddress', {
    container: document.getElementById('nomiDesc')
});

  new ClipboardJS('.copye6eAddress', {
    container: document.getElementById('e6eDesc')
});

  new ClipboardJS('.copyct2Address', {
    container: document.getElementById('ct2Desc')
});

  new ClipboardJS('.copyftbuAddress', {
    container: document.getElementById('ftbuDesc')
});

  new ClipboardJS('.copyobAddress', {
    container: document.getElementById('obDesc')
});

  new ClipboardJS('.copyhexxitAddress', {
    container: document.getElementById('hexxitDesc')
});
});

document.getElementById("body").onscroll = function myFunction() {  
    var scrolltotop = document.scrollingElement.scrollTop;
    var target = document.getElementById("headerBox");
    var xvalue = "center";
    var factor = 0.6;
    var yvalue = scrolltotop * factor;
    target.style.backgroundPosition = xvalue + " " + yvalue + "px";
  }