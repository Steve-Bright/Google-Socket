import socket

#this function asks for host and port number as parameter.
def get_response(host, port):
    # s is defined as null.     
    s = None

    try:
        # create a socket with ipv4 and tcp protocol
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # connect to the host and port number provided as parameter
        s.connect((host, port))

        # create a get request for the root path. 
        # the request is formatted as per HTTP protocol, with the method, path, version, host header and two newlines to indicate the end of headers.
        request = "GET / HTTP/1.0\r\nHost: " + host + "\r\n\r\n"

        # the request is sent to the connected server.
        s.send(request.encode())

        # server will respond with data. since the data will be received in chunks in bytes, we initialize an empty byte string to accumulate the response.
        response = b""

        #loop is used to receive data using recv() method, which reads up to 1024 bytes at a time. 
        # loop will stop working when there is no more data to receive, breaking the loop.
        while True:  
            data = s.recv(1024)
            if not data:
                break
            response += data

        #this function ends by decoding the accumulated bytes response into a string and returning it.
        return response.decode()

    #if there are any errors occur during the socket operations, they will be caught and printed, handling the error gracefully without crashing the program..
    except Exception as e:
        print("Socket error:", e)
        #The function will return None in case of an error.
        return None

    #after returning the response, the socket is closed.
    finally:
        if s is not None:
            s.close()


def separate_response(response):
    # since header and body are separted by two newlines,  "\r\n\r\n" is used to split the response into two parts. 
    headers, body = response.split("\r\n\r\n", 1)  #split only 1 time. 
    return headers, body


def extract_status(headers):
    #split the headers into separate lines.
    header_lines = headers.split("\r\n")

    #first line contains the http version, response code and response message.
    status_line = header_lines[0]
    http_version, response_code, response_message = status_line.split(" ", 2) #split 2 times.

    #store each part of the status line into separate variables.
    http_version = http_version
    response_code = int(response_code)
    response_message = response_message

    #return status details and the remaining header lines.
    return http_version, response_code, response_message, header_lines[1:]


def separate_headers(header_lines):
    #create an empty dictionary to store headers as key and value pairs.
    header_dict = {}

    #each header line is split by the first colon.
    for line in header_lines:
        if ":" in line:
            key, value = line.split(":", 1)
            header_dict[key.strip()] = value.strip()

    #return all headers in dictionary format.
    return header_dict


#main method 
if __name__ == "__main__":
    # call get_response with the host "www.google.com" and port 80 get the response.
    response = get_response("www.google.com", 80)

    #if response returns None, it fails to connect to the host. 
    if response is None:
        print("Failed to get response.")
    else:
        #if there is response, it will be first separated into header and body. 
        headers, body = separate_response(response)

        #header will be further extracted to get respective varaibles. 
        http_version, response_code, response_message, header_lines = extract_status(headers)

        #remaining header lines are converted into dictionary format.
        header_dict = separate_headers(header_lines)

        print("===========================STATUS===========================")
        print("HTTP Version:       ", http_version)
        print("Response Code:      ", response_code)
        print("Response Message:   ", response_message)

        print("===========================HEADERS===========================")
        for key, value in header_dict.items():
            print(f"{key}: {value}")

        print("===========================BODY===========================")

        if response_code != 200:
            print("Error: HTTP response is not 200.")
        else:
            print(body)
