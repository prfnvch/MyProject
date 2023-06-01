// document.addEventListener("DOMContentLoaded", function(event) { 
//     var scrollpos = localStorage.getItem('scrollpos');
//     if (scrollpos) window.scrollTo(0, scrollpos);
// });

// window.onbeforeunload = function(e) {
//     localStorage.setItem('scrollpos', window.scrollY);
// };

const rate = (rating, manga_id) => {
    fetch(`/rate/${manga_id}/${rating}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(rest => {
        window.location.reload();
        // you may want to update the rating here
        // to simplify stuff, I just reload the page
    })
}

var triggerTabList = [].slice.call(document.querySelectorAll('#myTab a'))
triggerTabList.forEach(function (triggerEl) {
  var tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', function (event) {
    event.preventDefault()
    tabTrigger.show()
  })
})


