from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib.parse

PORT = 8000

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/confirmar":
            query = urllib.parse.parse_qs(parsed_path.query)
            email = query.get("email", [""])[0]

            try:
                with open("usuarios.json", "r") as f:
                    usuarios = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                usuarios = {}

            usuarios[email] = {"confirmado": True}

            with open("usuarios.json", "w") as f:
                json.dump(usuarios, f, indent=4)

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("<h1>Confirmação recebida! Volte ao app.</h1>".encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    print(f"Servidor rodando em http://localhost:{PORT}")
    HTTPServer(("localhost", PORT), SimpleHandler).serve_forever()
