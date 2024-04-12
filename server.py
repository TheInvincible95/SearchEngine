from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import os
import search_engine


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        data = parse_qs(post_data)["query"][0]

        self.send_response(303)
        self.send_header("Location", "/results?data=" + data)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/img"):
            image_path = self.path.lstrip("/")
            image_file = os.path.join(
                os.getcwd(),
                image_path,
            )

            if os.path.exists(image_file):
                with open(image_file, "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-type", "image/png")
                    self.end_headers()
                    self.wfile.write(f.read())

        if self.path.startswith("/results"):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_content = """
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>rave Results</title>
                    <link rel="icon" type="image/png" href="img/magnifying-glass.png">
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

                        .search-button {
                            padding: 10px 20px;
                            font-size: 16px;
                            background-color: #4CAF50;
                            color: #fff;
                            border: none;
                            border-radius: 5px;
                            cursor: pointer;
                            transition: background-color 0.3s;
                        }

                        .search-button:hover {
                            background-color: #45a049;
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

                    </style>
                </head>
                <body>
                    <a href="#" id="scroll-to-top"></a>
                    <a href="http://localhost:8000/start" id="home"></a>
                    <div class="container">
                    <form class="search-form" action="#" method="post">
                        <input type="text" class="search-input" name="query" placeholder="Enter your search query" required>
                        <button type="submit" class="search-button"><img src="img/magnifying-glass.png" height="16"></button>
                    </form>
                        <ol class="results">
                """

            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            query = query_params["data"][0]

            results = search_engine.raveQuery(query)

            # Temporary hack till we clean our corpus
            # its permamnet now, shhhhh
            prev_doc = ""
            for item in results:
                name, ratings = item
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
            self.wfile.write(html_content.encode("utf-8"))

        elif self.path == "/start":
            with open("start.html", "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read())


def run():
    address = ("", 8000)
    server = HTTPServer(address, RequestHandler)
    print("Starting server...")
    server.serve_forever()


if __name__ == "__main__":
    run()
