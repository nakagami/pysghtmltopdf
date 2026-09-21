"""
python3 -mvenv .venv
. .venv/bin/activate
pip install flask sghtmltopdf
python flask_simple.py
"""

from io import BytesIO

import sghtmltopdf
from flask import Flask, send_file

html = "<html><body><h1>Hello, World!</h1><p>Generate PDF from HTML with Servo engine.</p></body></html>"

app = Flask(__name__)


@app.route("/")
def hello_root():
    return html


@app.route("/pdf")
def hello_pdf():
    pdf_data = sghtmltopdf.render(html)
    return send_file(
        BytesIO(pdf_data), mimetype="application/pdf", download_name="hello.pdf"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
