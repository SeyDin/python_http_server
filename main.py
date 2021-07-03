from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET request, Path:", self.path)
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(list_of_bytes_from_html("hello.html"))
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


def server_thread(server_port):
    server_address = ('', server_port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


def list_of_bytes_from_html(file_name):
    with open(os.curdir + os.sep + "view" + os.sep + file_name, 'rb') as file:
        list_of_bytes = b''.join(file.readlines())
        return list_of_bytes


if __name__ == '__main__':
    port = 8000
    print("Starting server at port %d" % port)
    server_thread(port)
