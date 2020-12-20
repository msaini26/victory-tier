
/**
 * Scrolls down the page
 */

document.getElementById("myDiv").onscroll = function(){scroll()};

function scroll() {
   document.getElementyById("test").innerHTML = "YOU SCROLLED IN DIV.";
   window.scroll(0,100);
}

/**
 * Performs a search and updates the DOM.
 * Note: this function is asynchronous
 */
function search() {
	// TODO Implement
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
