// Creating a XHR object
let req = new XMLHttpRequest();
let server = "http://localhost:8000/test";

// open a connection
req.open("POST", server, true);

let url = window.location.href;
let title = document.title;
let body = document.body.innerText;

// Converting JSON data to string
var data = JSON.stringify({ "url": url, "title": title, "body": body });

// Sending data with the request
req.send(data);
