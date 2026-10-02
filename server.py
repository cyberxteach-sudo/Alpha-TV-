import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = "hls"

os.makedirs(DIRECTORY, exist_ok=True)

class SecureHLSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # Allow access ONLY to streaming playlist and segments
        allowed_extensions = ('.m3u8', '.ts')
        
        if self.path == '/' or not self.path.endswith(allowed_extensions):
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>403 Forbidden - Access Denied</h1>")
            return
            
        return super().do_GET()

with socketserver.TCPServer(("", PORT), SecureHLSHandler) as httpd:
    print(f"[+] Secure Server hosting '{DIRECTORY}' on port {PORT}")
    httpd.serve_forever()
      
