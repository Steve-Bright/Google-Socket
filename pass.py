import socket

def getResponse(host, port):
    try: 
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        request = "GET / HTTP/1.0\r\nHost: " + host + "\r\n\r\n"
        s.send(request.encode())
        response = b""
        while True:
            data = s.recv(1024) #1024 bytes
            if not data:
                break
            response += data
        s.close()
        return response.decode()
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    response = getResponse("www.google.com", 80)
    print(response)