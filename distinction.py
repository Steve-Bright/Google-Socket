import socket
import re

#this function gets a response from the provided host, port and path.
def fetch_url(host, port, path):
    # s is defined as null.
    s = None
    try: 
        # create a socket with ipv4 and tcp protocol.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the host and port number provided as parameter.
        s.connect((host, port))

        # create a get request using the path provided.
        request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"

        # send the request to the server.
        s.sendall(request.encode())

        # create an empty byte string to store the response.
        response = b""

        # receive the response in chunks until no more data is received.
        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data

        # return the full response in bytes.
        return response
    
    except Exception as e:
        print("Socket error:", e)
        #The function will return None in case of an error.
        return None

    #after returning the response, the socket is closed.
    finally:
        if s is not None:
            s.close()
    


def split_http_response(response):
    # headers and body are separated by two newlines.
    return response.split(b"\r\n\r\n", 1)


def get_status_code(headers):
    # first line of the header contains the status code.
    status_line = headers.decode(errors="ignore").split("\r\n")[0]
    return int(status_line.split(" ")[1])


def extract_img_src(html):
    # find all image source links from img tags.
    return re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE)


def build_full_url(base_host, src):
    # Case 1: already full URL
    if src.startswith("http://"):
        parts = src.replace("http://", "").split("/", 1)
        host = parts[0]
        path = "/" + parts[1] if len(parts) > 1 else "/"
        return host, path

    # Case 2: relative path
    if src.startswith("/"):
        return base_host, src

    # Case 3: relative without slash
    return base_host, "/" + src


def extract_filename(path, index):
    # get the filename from the image path.
    filename = path.split("/")[-1]

    # use a default filename if the path has no filename.
    if filename == "":
        filename = f"image_{index}.img"

    return filename


if __name__ == "__main__":
    # set host, port and path to request.
    host = "www.google.com"
    port = 80
    path = "/"

    # fetch the main webpage response.
    response = fetch_url(host, port, path)

    # separate the response into headers and body.
    headers, body = split_http_response(response)

    # get the response status code.
    status_code = get_status_code(headers)

    if status_code != 200:
        print("Error: HTTP response is not 200")
    else:
        # decode the body into html text.
        html = body.decode(errors="ignore")

        # extract all image sources from the html.
        img_sources = extract_img_src(html)
        print("image sources found:", img_sources)

        print("Images found:", len(img_sources))

        # loop through each image source and download it.
        for i, src in enumerate(img_sources, start=1):
            # convert image source into host and path.
            img_host, img_path = build_full_url(host, src)

            # get a filename for the downloaded image.
            filename = extract_filename(img_path, i)

            print("Downloading:", img_host + img_path)

            # fetch the image response.
            img_response = fetch_url(img_host, 80, img_path)

            # separate image response into headers and body.
            img_headers, img_body = split_http_response(img_response)

            if get_status_code(img_headers) == 200:
                # save the image body into a file.
                with open(filename, "wb") as f:
                    f.write(img_body)
            else:
                print("Failed:", img_host + img_path)
