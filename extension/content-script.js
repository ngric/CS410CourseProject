console.log("this shit work?");
console.log(text);

let page = window.location.href;
var text = document.body.innerText;

// Creating a XHR object
let xhr = new XMLHttpRequest();
let url = "http://localhost:8000/test";

// open a connection
xhr.open("POST", url, true);

// Set the request header i.e. which type of content you are sending
// xhr.setRequestHeader("Content-Type", "application/json");

// Create a state change callback
// xhr.onreadystatechange = function () {
//     if (xhr.readyState === 4 && xhr.status === 200) {

// 	// Print received data from server
// 	result.innerHTML = this.responseText;

//     }
// };

// Converting JSON data to string
var data = JSON.stringify({ "url": page, "body": text });

// Sending data with the request
xhr.send(data);
