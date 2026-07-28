from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
import json
import joblib

ROOT = Path(__file__).resolve().parent
INDEX_PATH = ROOT / "index.html"
MODEL_PATH = ROOT / "sentiment_analysis_model.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

model = joblib.load(MODEL_PATH)


class SentimentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in {"/", "/index.html"}:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(INDEX_PATH.read_bytes())
            return

        self.send_error(404, "Page not found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/predict":
            self.send_error(404, "Endpoint not found")
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length).decode("utf-8")

        try:
            payload = json.loads(body or "{}")
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON payload"})
            return

        text = (payload.get("text") or "").strip()
        if not text:
            self._send_json(400, {"error": "Please enter a sentence first."})
            return

        prediction = model.predict([text])[0]
        self._send_json(200, {"sentiment": prediction, "text": text})

    def _send_json(self, status_code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8000
    print(f"Serving sentiment app at http://{host}:{port}")
    ThreadingHTTPServer((host, port), SentimentHandler).serve_forever()
