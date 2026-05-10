## Credit
Connects to a web server using raw TCP sockets, sends an HTTP GET request, receives the HTTP response, and separates the response into headers and body.

## Features
- Sends HTTP/1.0 GET requests
- Extracts HTTP version, response code, and response message
- Separates headers into dictionary format
- Displays webpage HTML content

---
## Distinction
Connects to a website using raw TCP sockets, extracts image sources from the HTML, downloads the images, and saves them locally.

## Features
- Sends HTTP/1.0 GET requests
- Extracts image URLs from HTML using regex
- Downloads images from the website
- Saves images using their original filenames
