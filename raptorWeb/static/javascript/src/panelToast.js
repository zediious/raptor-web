function createToast(message) {
    // Clone the template
    const element = htmx.find("[data-toast-template]").cloneNode(true)
    
    // Remove the data-toast-template attribute
    delete element.dataset.toastTemplate
    
    // Set the CSS class
    if (message.tags == "error") {
        element.className += " " + "text-bg-danger"
    } else {
        element.className += " " + "text-bg-success"
    }
    
    // Set the text
    htmx.find(element, "[data-toast-body]").innerText = message.message
    
    // Add the new element to the container
    htmx.find("[data-toast-container]").appendChild(element)
    
    // Show the toast using Bootstrap's API
    const toast = new bootstrap.Toast(element, { delay: 4000 })
    toast.show()
}
  

htmx.on("messages", (e) => {
    e.detail.value.forEach(createToast)
  })
  