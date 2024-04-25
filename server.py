from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import os
import search_engine
from jinja2 import Template
import json
import mimetypes
import subprocess
import csv


def read_labels_csv(file_path):
    data = []
    with open(file_path, "r", newline="") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            data.append(row[1].strip())
    return data


labels_data = read_labels_csv("labels.csv")


def extract_cookie(self):
    # Extracting cookie back
    cookie_header = self.headers.get("Cookie")
    cookies = {}
    if cookie_header:
        cookie_pairs = cookie_header.split(";")
        for pair in cookie_pairs:
            key, value = pair.strip().split("=")
            cookies[key] = value
    try:
        return list(cookies["rave_cat_data"][1:-1])
    except KeyError:
        return []


def serve_static(self):
    file_path = self.path.lstrip("/")
    if os.path.exists(file_path):
        content_type, _ = mimetypes.guess_type(file_path)
        with open(file_path, "rb") as f:
            self.send_response(200)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(f.read())
    else:
        self.send_error(404, "File not found")


# Speech-to-text subprocess
process = None


class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        query = parse_qs(post_data)
        data = query["query"][0]

        # Store user chosen categories as cookie
        category = ""
        if "cat" in query:
            for label in range(5):
                if str(label) in query["cat"]:
                    category += str(label)
        cookie_data = json.dumps(category)

        self.send_response(303)
        self.send_header("Content-type", "text/html")
        self.send_header("Set-Cookie", f"rave_cat_data={cookie_data}; SameSite=Strict")
        self.send_header("Location", "/results?data=" + data)
        self.end_headers()

    def do_GET(self):
        global process

        if self.path == "/trigger-STT":
            if process is None:
                # Start the python STT process
                process = subprocess.Popen(
                    ["python", "speechToText.py"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                stdout, stderr = process.communicate()
                data = stdout.decode("utf-8").strip()
                self.send_response(200)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(data.encode("utf-8"))
                process = None

        elif self.path.startswith("/results"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")

            category = extract_cookie(self)
            self.end_headers()

            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            query = query_params["data"][0]

            results = search_engine.raveQuery(category, query)

            with open("results.html", "r") as f:
                template = Template(f.read())
                category = extract_cookie(self)
                rendered_html = template.render(
                    category=category,
                    results=results,
                    labels_data=labels_data,
                    documents=search_engine.documents,
                    query=query,
                )
                self.wfile.write(rendered_html.encode("utf-8"))

        elif self.path == "/start":
            with open("start.html", "r") as f:
                template = Template(f.read())
                category = extract_cookie(self)
                rendered_html = template.render(category=category)
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(rendered_html.encode("utf-8"))

        else:
            serve_static(self)


def run():
    address = ("", 8000)
    server = HTTPServer(address, RequestHandler)
    print("Starting server...")
    server.serve_forever()


if __name__ == "__main__":
    run()
