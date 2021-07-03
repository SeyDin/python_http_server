from http.server import BaseHTTPRequestHandler, HTTPServer
import os

html = '<html><body><h3>Hello from the Raspberry Pi</h3><img src="sam.jpg"/></body></html>'


class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("GET request, Path:", self.path)
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open(os.curdir + os.sep + "view" + os.sep + "hello.html", 'rb') as file:
                self.wfile.write(string_from_html("hello.html").encode('utf-8'))
        elif self.path.endswith(".jpg"):
            self.send_response(200)
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            with open(os.curdir + os.sep + "view" + os.sep + "images" + os.sep + self.path, 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))


def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


def string_from_html(file_name):
    with open(os.curdir + os.sep + "view" + os.sep + file_name, 'rb') as file:
        string = "".join([x.strip().decode("utf-8") for x in file.readlines()])
        return string


if __name__ == '__main__':
    port = 8000
    print("Starting server at port %d" % port)
    server_thread(port)