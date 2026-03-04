from http.server import BaseHTTPRequestHandler, HTTPServer

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type","text/plain")
        self.end_headers()
        self.wfile.write(b"Server is running smoothly!")
        self.wfile.write(b"the last test was successful!")

PORT = 5000

print("Server Started...")
server = HTTPServer(("0.0.0.0", PORT), handler)
server.serve_forever()
print("NEW VERSION!")