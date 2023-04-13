import requests
import signal
import sys
import urllib.parse
import threading
#import ssl
from socketserver import ThreadingMixIn
from http.server import SimpleHTTPRequestHandler, BaseHTTPRequestHandler, HTTPServer

#DIRECTORY="C:\\Users\\PC\\Dev\\xaza\\kodi-white-noise-vite\\dist"
DIRECTORY="/storage/react-player"
PORT=80 #8087

class ProxyHTTPRequestHandler(SimpleHTTPRequestHandler):       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        super().do_GET()


    def do_POST(self, body=True):
        try:
            url = self._resolve_url()
            content_len = int(self.headers["content-length"])
            post_body = self.rfile.read(content_len)
            req_header = self.parse_headers()

            resp = requests.post(url, data=post_body, headers=req_header, verify=False)

            self.send_response(resp.status_code)
            self.send_resp_headers(resp)
            if body:
                self.wfile.write(resp.content)
        except:
            self.send_error(500, 'error trying to proxy')
                

    def parse_headers(self):
        req_header = {}
        for line in self.headers:
            line_parts = [o.strip() for o in line.split(':', 1)]
            if len(line_parts) == 2:
                req_header[line_parts[0]] = line_parts[1]
        return req_header

    def send_resp_headers(self, resp):
        respheaders = resp.headers
        self.send_cors_headers()
        for key in respheaders:
            if key not in ['Content-Encoding', 'Transfer-Encoding', 'content-encoding', 'transfer-encoding', 'content-length', 'Content-Length']:
                self.send_header(key, respheaders[key])
        self.send_header('Content-Length', len(resp.content))
        self.end_headers()

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header('Access-Control-Allow-Private-Network', 'true')

    def _resolve_url(self):
        return "http://127.0.0.1:8089/jsonrpc"

ProxyHTTPRequestHandler.extensions_map={
    '.manifest': 'text/cache-manifest',
    '.html': 'text/html',
    '.png': 'image/png',
    '.jpg': 'image/jpg',
    '.svg':	'image/svg+xml',
    '.css':	'text/css',
    '.js':	'application/x-javascript',
    '.json': 'application/json',
    '': 'application/octet-stream', # Default
}

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def run():
    #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    #context.load_cert_chain("/storage/proxy/cert.pem", "/storage/proxy/key.pem", "fall0ut1")
    server = ThreadedHTTPServer(('0.0.0.0', PORT), ProxyHTTPRequestHandler)
    #server.socket = context.wrap_socket(server.socket, server_side=True)
    print('proxy server is running')
    server.serve_forever()

    
def exit_now(signum, frame):
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGTERM, exit_now)
    run()