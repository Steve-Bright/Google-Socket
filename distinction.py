import socket
import re
import os

def fetch_url(host, path):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 80))

    request = f"GET {path} HTTP/1.0\r\nHost: {host}\r\n\r\n"
    s.sendall(request.encode())

    response = b""

    while True:
        data = s.recv(1024)
        if not data:
            break
        response += data

    s.close()
    return response


def split_http_response(response):
    return response.split(b"\r\n\r\n", 1)


def get_status_code(headers):
    status_line = headers.decode(errors="ignore").split("\r\n")[0]
    return int(status_line.split(" ")[1])


def extract_img_src(html):
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
    filename = path.split("/")[-1]

    if filename == "":
        filename = f"image_{index}.img"

    return filename


if __name__ == "__main__":
    host = "www.google.com"
    path = "/"

    response = fetch_url(host, path)
    headers, body = split_http_response(response)

    status_code = get_status_code(headers)

    if status_code != 200:
        print("Error: HTTP response is not 200")
    else:
        html = body.decode(errors="ignore")

        img_sources = extract_img_src(html)
        print("image sources found:", img_sources)

        print("Images found:", len(img_sources))

        for i, src in enumerate(img_sources, start=1):
            img_host, img_path = build_full_url(host, src)
            filename = extract_filename(img_path, i)

            print("Downloading:", img_host + img_path)

            img_response = fetch_url(img_host, img_path)
            img_headers, img_body = split_http_response(img_response)

            if get_status_code(img_headers) == 200:
                with open(filename, "wb") as f:
                    f.write(img_body)
            else:
                print("Failed:", img_host + img_path)