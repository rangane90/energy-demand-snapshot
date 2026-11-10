import argparse
import csv
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from statistics import mean
from urllib.parse import urlsplit


def summarize(path):
    with path.open(encoding="utf-8", newline="") as source:
        readings = [int(row["demand_mw"]) for row in csv.DictReader(source)]

    return {
        "data_source": "synthetic",
        "samples": len(readings),
        "average_mw": round(mean(readings), 2),
        "peak_mw": max(readings),
    }


def make_server(host, port):
    summary = summarize(Path(__file__).with_name("sample_demand.csv"))
    routes = {"/health": {"status": "ok"}, "/summary": summary}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            payload = routes.get(urlsplit(self.path).path)
            status = 200 if payload is not None else 404
            body = json.dumps(payload if payload is not None else {"error": "not found"}).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serve a synthetic electricity-demand snapshot.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8080, type=int)
    args = parser.parse_args()
    with make_server(args.host, args.port) as server:
        print(f"Listening on http://{args.host}:{server.server_port}", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
