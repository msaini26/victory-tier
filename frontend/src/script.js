
/**
 * Scrolls down the page
 */

document.getElementById("myDiv").onscroll = function(){scroll()};

function scroll() {
   document.getElementById("test").innerHTML = "YOU SCROLLED IN DIV.";
}

/**
 * Performs a search and updates the DOM.
 * Note: this function is asynchronous
 */
function search() {
	// Get the search text
	let query = document.getElementById("search-box").value;

	// Make XHR request for the server data
	fetch('http://localhost:5000/search', { method: 'POST', body: '{"search": "LeBron"}'})

	const requestBody = JSON.stringify({search: query})
	const request = new Request('/search',
		{
			method: 'POST',
			body: requestBody,
		}
	)
	fetch(request).then(response => console.log(response))
}


/**
 * Callback for when the user searches for a player
 */
function onSearch() {
	search();
	scroll();
}

/**
 * Main application entrypoint
 */
function main() {

}

window.onload = main;
