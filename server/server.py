from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        print("\n----- Request Start ----->\n")
        print(self.path)
        print(self.headers)
        print("<----- Request End -----\n")

        if (self.path == '/test.html'):
            with open('test.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            message = "Hello, World! Here is a GET response"
            self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()


        print("\n----- Request Start ----->\n")

        print(self.path)
        print(self.headers)
        length = int(self.headers['Content-Length'])
        message = self.rfile.read(length)
        data = json.loads(message)
        print(data['url'])
        print(data['body'])

        print("<----- Request End -----\n")

        message = "Hello, World! Here is a POST response"
        self.wfile.write(bytes(message, "utf8"))

with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()
