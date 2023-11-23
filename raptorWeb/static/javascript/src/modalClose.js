function closeOffCanvas() {

  let closeCanvas = document.querySelector('[data-bs-dismiss="offcanvas"]');
  closeCanvas.click();

}

function closeModal() {

  $('.modal').modal('hide');
  console.log("did run closeModal")

}
  