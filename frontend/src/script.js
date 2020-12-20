
/**
 * Scrolls down the page
 */

document.getElementById("myDiv").onscroll = function(){scroll()};

function scroll() {
   document.getElementById("test").innerHTML = "YOU SCROLLED IN DIV.";
   window.scroll(0,100);
}

/**
 * Performs a search and updates the DOM.
 * Note: this function is asynchronous
 */
function search() {
	// Get the search text
	let query = document.getElementById("search-box").value;

	// Make XHR request for the server data
	const requestBody = {search: query};
	const request = new Request('/search',
		{
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(requestBody)
		}
	)
	fetch(request).then(response => response.json()).then(json => {
		console.log(json);
	})

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
