import os
from http.server import BaseHTTPRequestHandler


class StaticServer:
    STATIC_DIR = 'static'

    @classmethod
    def handle_static(request_handle: BaseHTTPRequestHandler):
        if request_handle.path.startswith('/static/'):
            file_path = "."+request_handle.path
        else:
            return False

        if os.path.exists(file_path) and os.path.isfile(file_path):
            request_handle.send_response(200)

            mime_types = {
                '.css': 'text/css',
                '.js': 'text/javascript',
                '.png': 'image/png',
                '.svg': 'image/svg+xml',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif'
            }

            ext = os.path.splitext(file_path)[1]
            content_type = mime_types.get(ext, "application/octet-stream")

            request_handle.send_header('Content-Type', content_type)

            request_handle.end_headers()

            with open(file_path, 'rb') as file:
                request_handle.wfile.write(file.read())
                return True
        else:
            request_handle.send_response(404)
            request_handle.end_headers()
            request_handle.wfile.write(b'404 Not Found')
            return True