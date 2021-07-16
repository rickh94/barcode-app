from flask import Flask, send_file, request, render_template
from werkzeug.exceptions import abort

import name_label
import number_label
from combine_into_pages import turn_labels_into_output

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/labels", methods=["POST"])
def create_labels():
    data = request.get_json()
    numbers = data.get("numbers")
    if not numbers:
        abort(400)

    output_pdf = turn_labels_into_output(
        [number_label.make_label(num) for num in numbers]
    )

    return send_file(output_pdf)


@app.route("/name-labels", methods=["POST"])
def create_name_labels():
    data = request.get_json()
    names = data.get("names")
    if not names:
        abort(400)

    output_pdf = turn_labels_into_output(
        [name_label.make_label(name) for name in names]
    )

    return send_file(output_pdf)
