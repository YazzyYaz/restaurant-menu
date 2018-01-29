from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web Server running on port {}".format(port))
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C Entered, stopping web server...")
        server.socket.close()

if __name__ == "__main__":
    main()
