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
                self.wfile.write(data.encode("utf-8"))
                process = None

        elif self.path.startswith("/results"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")

            category = extract_cookie(self)
            self.end_headers()

            html_content = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>rave Results</title>
                    <link rel="icon" type="image/png" href="img/magnifying-glass.png">
                    <script src="script.js"></script>
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-image: url('img/art.jpg');
                        }
                        .container {
                            max-width: 800px;
                            margin: 100px auto;
                            padding: 20px;
                            background-color: #828658;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 1.0);
                            border-radius: 5px;
                        }
                        .search-form {
                            text-align: center;
                            padding: 20px;
                        }

                        .search-input {
                            width: 60%;
                            padding: 10px;
                            font-size: 16px;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                            outline: none;
                        }

                        .search-button,
                        .record-button {
                            padding: 10px 20px;
                            font-size: 16px;
                            background-color: #4CAF50;
                            color: #fff;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            transition: background-color 0.3s;
                        }

                        .record-button {
                            width: 90px;
                        }

                        .search-button:hover,
                        .record-button:hover {
                            background-color: #45a049;
                        }

                        .record-button #timer,
                        .record-button #loader {
                            display: inline-block;
                            position: relative;
                            top: -1px;
                            margin-left: 5px;
                        }

                        summary::-webkit-details-marker {
                            display: none;
                        }

                        summary {
                            list-style: none;
                            cursor: pointer;
                        }

                        summary:hover h3{
                            text-decoration: underline;
                        }

                        #scroll-to-top {
                            background-image: url('img/up-arrow.png');
                            position: fixed;
                            bottom: 20px;
                            right: 20px;
                            z-index: 99;
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 50%;
                            padding: 15px;
                            cursor: pointer;
                            width: 30px;
                            height: 30px;
                            background-repeat: no-repeat;
                            background-size: 35px;
                            background-position: center;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 1.0);
                        }

                        #scroll-to-top:hover {
                            background-color: #45A049;
                        }

                        #home {
                            background-image: url('img/home.png');
                            position: fixed;
                            bottom: 20px;
                            left: 20px;
                            z-index: 99;
                            background-color: #4CAF50;
                            color: white;
                            border: none;
                            border-radius: 50%;
                            padding: 15px;
                            cursor: pointer;
                            width: 30px;
                            height: 30px;
                            background-repeat: no-repeat;
                            background-size: 35px;
                            background-position: center;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 1.0);
                        }

                        input[type="checkbox"] {
                            display: none;
                        }

                        .category {
                            display: flex;
                            margin-top: 20px;
                            padding: 5px;
                            justify-content: center;
                            align-items: center;
                            transform: translateX(-10px);
                        }

                        .custom-checkbox {
                            margin-left: 20px;
                            display: inline-block;
                            width: 12px;
                            height: 12px;
                            background-color: #fff;
                            border: 1px solid #000000;
                            border-radius: 3px;
                            cursor: pointer;
                        }

                        input[type="checkbox"]:checked+.custom-checkbox {
                            background-color: #45a049;
                        }

                        #loader {
                            border: 4px solid #000000;
                            border-top: 4px solid #ffffff;
                            border-radius: 50%;
                            width: 8px;
                            height: 8px;
                            animation: spin 1s linear infinite;
                        }

                        @keyframes spin {
                            0% {
                                transform: rotate(0deg);
                            }

                            100% {
                                transform: rotate(360deg);
                            }
                        }

                        @font-face {
                            font-family: 'oldenburg';
                            src: url('fonts/oldenburg.woff2') format('woff2');
                        }

                        .no-results{
                            text-align: center;
                        }

                    </style>
                    <noscript>
                        <style>
                            .record-button,
                            .record-button:hover {
                                background-color: #959595;
                            }
                        </style>
                    </noscript>
                </head>
                <body>
                    <a href="#" id="scroll-to-top"></a>
                    <a href="http://localhost:8000/start" id="home"></a>
                    <div class="container">
                    <form class="search-form" action="#" method="post">
                        <input type="text" class="search-input" name="query" placeholder="Enter your search query" required>
                        <button type="submit" class="search-button"><img src="img/magnifying-glass.png" height="16"></button>
                        <button type="button" class="record-button" onclick="toggleMic()"><img id="mic-img"
                            src="img/microphone-black-shape.png" height="16">
                        <div id="timer">3s</div>
                        </button>
                        <div class="category">
                            <label>
                                <input type="checkbox" name="cat" value="0" {% for item in category %}{% if item == "0" %} checked {% endif %}{% endfor %}>
                                <span class="custom-checkbox"></span>
                                {% if "0" in category %}<span style="text-decoration: underline;">{% endif %}Politics{% if "0" in category %}</span>{% endif %}
                            </label>
                            <label>
                                <input type="checkbox" name="cat" value="1" {% for item in category %}{% if item == "1" %}checked{% endif %}{% endfor %}>
                                <span class="custom-checkbox"></span>
                                {% if "1" in category %}<span style="text-decoration: underline;">{% endif %}Sport{% if "1" in category %}</span>{% endif %}
                            </label>
                            <label>
                                <input type="checkbox" name="cat" value="2" {% for item in category %}{% if item == "2" %}checked{% endif %}{% endfor %}>
                                <span class="custom-checkbox"></span>
                                {% if "2" in category %}<span style="text-decoration: underline;">{% endif %}Technology{% if "2" in category %}</span>{% endif %}
                            </label>
                            <label>
                                <input type="checkbox" name="cat" value="3" {% for item in category %}{% if item == "3" %} checked {% endif %}{% endfor %}>
                                <span class="custom-checkbox"></span>
                                {% if "3" in category %}<span style="text-decoration: underline;">{% endif %}Entertainment{% if "3" in category %}</span>{% endif %}
                            </label>
                            <label>
                                <input type="checkbox" name="cat" value="4" {% for item in category %}{% if item == "4" %}checked{% endif %}{% endfor %}>
                                <span class="custom-checkbox"></span>
                                {% if "4" in category %}<span style="text-decoration: underline;">{% endif %}Business{% if "4" in category %}</span>{% endif %}
                            </label>
                        </div>
                    </form>
                        <ol class="results">
                """

            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            query = query_params["data"][0]

            results = search_engine.raveQuery(category, query)

            if results == []:
                html_content += """</ol>
                    <div class="no-results">
                        <img src="img/argonath.png" height="350px">
                        <h2 style="font-family:oldenburg;"> Stop! You have exhausted us :} Perhaps try searching with a better query next time... </h2>
                    </div>
                    <ol>
                """
            else:
                # Temporary hack till we clean our corpus
                # its permanent now, shhhhh
                prev_doc = ""
                for item in results:
                    name, ratings, cat = item
                    label = labels_data[int(cat) + 1]
                    doc = search_engine.documents[name]
                    if doc == prev_doc:
                        continue
                    prev_doc = doc
                    title = doc.splitlines()[0]
                    desc_line = doc.splitlines()[2]
                    content = "".join(doc.splitlines()[4:])
                    html_content += f"""
                                <li>
                                    <div class="result-title">
                                    <details>
                                        <summary>
                                            <h3>{title}</h3>
                                            <p><i>[{label}]</i></p>
                                            <p>{desc_line}</p>                                         
                                        </summary>
                                        <p>{content}</p>
                                    </details>
                                    </div>
                                </li>
                    """
            html_content += """
                        </ol>
                    </div>
                </body>
                </html>
                """
            template = Template(html_content)
            rendered_html = template.render(category=category)
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
