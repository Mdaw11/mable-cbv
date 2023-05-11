const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-btn");

// show sidebar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

// close sidebar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})

// change theme
themeToggler.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme-variables');

    themeToggler.querySelector('span').classList.toggle('active');
})

// Notification dropdown
$(document).ready(function() {
    $(".notification-drop .item").on('click',function() {
      $(this).find('ul').toggle();
    });
});

// NOTIFICATION DROPDOWN

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */

function markAsRead(element) {
	var notificationId = element.getAttribute('data-notification-id');
	var url = '/mark_notification_as_read/' + notificationId + '/';
	var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  
	fetch(url, {
	  method: 'POST',
	  headers: {
		'Content-Type': 'application/json',
		'X-CSRFToken': csrfToken
	  },
	  body: JSON.stringify({})
	})
	.then(response => response.json())
	.then(data => {
	  if (data.success) {
		// update the badge count
		var count = document.querySelector('.badge');
		count.textContent = parseInt(count.textContent) - 1;
  
		// redirect to the ticket page
		var ticketUrl = element.getAttribute('href');
		window.location.href = ticketUrl;
	  }
	})
	.catch(error => console.error(error));
}
// NOTIFICATION DROPDOWN END