import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from Servers.static_server import StaticServer


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if StaticServer.handle_static(self):
            return
        elif self.path == "/":
            self.path = "/index.html"

        try:
            with open("templates" + self.path, "r", encoding="utf-8") as file:
                content = file.read()
                self.send_response(200)
        except FileNotFoundError:
            content = "404 Not Found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


def web(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, Server)
    print("Server running at port", port)
    httpd.serve_forever()


if __name__ == '__main__':
    web(7878)