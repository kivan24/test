import BaseHTTPServer
import SimpleHTTPServer
import ssl

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open("index.html", "r") as f:
            self.wfile.write(f.read())

if __name__ == '__main__':
    host = ''
    port = 443
    httpd = BaseHTTPServer.HTTPServer((host, port), MyHandler)
    
    # Завантаження pem-сертифікату
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile='./server.pem', server_side=True)
    
    print('Сервер слухає на порту {}: https://{}:{}'.format(port, host, port))
    httpd.serve_forever()
