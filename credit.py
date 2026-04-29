import socket

def get_response(host, port):
    s = None

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        request = "GET / HTTP/1.0\r\nHost: " + host + "\r\n\r\n"

        s.send(request.encode())

        response = b""

        while True:
            data = s.recv(1024)
            if not data:
                break
            response += data

        return response.decode()

    except Exception as e:
        print("Socket error:", e)
        return None

    finally:
        if s is not None:
            s.close()


def separate_response(response):
    headers, body = response.split("\r\n\r\n", 1)
    return headers, body


def extract_status(headers):
    header_lines = headers.split("\r\n")

    status_line = header_lines[0]
    parts = status_line.split(" ", 2)

    http_version = parts[0]
    response_code = int(parts[1])
    response_message = parts[2] if len(parts) > 2 else ""

    return http_version, response_code, response_message, header_lines[1:]


def separate_headers(header_lines):
    header_dict = {}

    for line in header_lines:
        if ":" in line:
            key, value = line.split(":", 1)
            header_dict[key.strip()] = value.strip()

    return header_dict


if __name__ == "__main__":
    response = get_response("www.test.com", 80)

    if response is None:
        print("Failed to get response.")
    else:
        headers, body = separate_response(response)

        http_version, response_code, response_message, header_lines = extract_status(headers)

        header_dict = separate_headers(header_lines)

        print("===========================STATUS===========================")
        print("HTTP Version:", http_version)
        print("Response Code:", response_code)
        print("Response Message:", response_message)

        print("===========================HEADERS===========================")
        for key, value in header_dict.items():
            print(f"{key}: {value}")

        print("===========================BODY===========================")

        if response_code != 200:
            print("Error: HTTP response is not 200.")
        else:
            print(body)