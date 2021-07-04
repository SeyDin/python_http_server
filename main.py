import os
import json

from io import BytesIO
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET request, Path:", self.path)
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(string_of_bytes_from_html("hello.html"))
        elif self.path.endswith(".jpg"):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            with open(os.curdir + os.sep + "view" + os.sep + "images" + os.sep + self.path, 'rb') as file:
                self.wfile.write(file.read())
        elif self.path.endswith(".css"):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open(os.curdir + os.sep + "view" + os.sep + "css" + os.sep + self.path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        params = json.loads(urlparse(body).path.decode("utf-8"))
        print(params)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


def server_thread(server_port):
    server_address = ('', server_port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


def string_of_bytes_from_html(file_name):
    with open(os.curdir + os.sep + "view" + os.sep + file_name, 'rb') as file:
        string_of_bytes = b''.join(file.readlines())
        return string_of_bytes


if __name__ == '__main__':
    port = 8000
    print("Starting server at port %d" % port)
    server_thread(port)
