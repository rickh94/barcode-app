import tempfile
import uuid

import PyPDF2
from PIL import Image, ImageDraw, ImageFont, ImageOps
from flask import Flask, send_file, request, render_template
from pathlib import Path

# noinspection PyUnresolvedReferences
import barcode
from werkzeug.exceptions import abort

PIXELS_PER_IN = 300


def in_to_px(inches):
    return int(inches * PIXELS_PER_IN)


PAGE_WIDTH_IN = 8.5
PAGE_HEIGHT_IN = 11
PAGE_WIDTH_PX = in_to_px(PAGE_WIDTH_IN)
PAGE_HEIGHT_PX = in_to_px(PAGE_HEIGHT_IN)

LABEL_WIDTH_IN = 2
LABEL_HEIGHT_IN = 3
LABEL_WIDTH_PX = in_to_px(LABEL_WIDTH_IN)
LABEL_HEIGHT_PX = in_to_px(LABEL_HEIGHT_IN)

LABELS_PER_ROW = int(PAGE_WIDTH_IN / LABEL_WIDTH_IN)
ROWS_PER_PAGE = int(PAGE_HEIGHT_IN / LABEL_HEIGHT_IN)
FONT = ImageFont.truetype("./PTSans-Regular.ttf", 35)

WHITE = "#ffffff"
VERY_LIGHT_GRAY = "#c0c0c0"

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

    labels = [make_label(num) for num in numbers]
    rows = make_image_rows(labels)
    tmp = tempfile.TemporaryDirectory()
    last_page = make_pages(rows, tmp.name)
    output_pdf = combine_pages(tmp.name, Path("/output"), last_page)
    tmp.cleanup()

    return send_file(output_pdf)


def make_label(number: str):
    tmp = tempfile.TemporaryDirectory()
    barcode.generate_instrument_barcode(number, tmp.name, 3, 70)
    property_of_tmm = Image.open("./property-of-tmm-image.png")
    code = Image.open(f"{tmp.name}/{number}.png")

    label_image = Image.new("RGB", (LABEL_WIDTH_PX, LABEL_HEIGHT_PX), color="#ffffff")
    label_image.paste(property_of_tmm, (0, 0))
    x_offset = int((LABEL_WIDTH_PX - code.width) / 2)
    y_offset = property_of_tmm.height + 15
    label_image.paste(code, (x_offset, y_offset))

    d = ImageDraw.Draw(label_image)
    d.text(
        xy=(LABEL_WIDTH_PX // 2, y_offset + code.height + 40),
        text=number,
        fill="#000000",
        anchor="ms",
        font=FONT,
    )
    tmp.cleanup()
    return label_image


def make_image_rows(labels):
    row = []
    all_rows = []

    for label in labels:
        if len(row) == LABELS_PER_ROW:
            all_rows.append(make_row(row))
            row = []
        row.append(label)
    if row:
        all_rows.append(make_row(row))

    return all_rows


def make_row(labels):
    x_offset = in_to_px(0.12)
    new_row = Image.new("RGB", (PAGE_WIDTH_PX, LABEL_HEIGHT_PX - 2), color=WHITE)
    for idx, label in enumerate(labels):
        border = (2, 0, 0, 0)
        if idx == len(labels) - 1:
            border = (2, 0, 2, 0)
        next_im = ImageOps.expand(label, border=border, fill=VERY_LIGHT_GRAY)
        new_row.paste(next_im, (x_offset, 0))
        x_offset += label.width + in_to_px(0.12) - 2
    return ImageOps.expand(new_row, border=(0, 2, 0, 2), fill=VERY_LIGHT_GRAY)


def make_pages(rows, location):
    rows_in_page = []
    current_page = 0
    for row in rows:
        if len(rows_in_page) == ROWS_PER_PAGE:
            write_page(rows_in_page, current_page, location)
            rows_in_page = []
            current_page += 1
        rows_in_page.append(row)

    if rows_in_page:
        write_page(rows_in_page, current_page, location)
    return current_page


def write_page(rows_in_page, page_number, location):
    page = Image.new("RGB", (PAGE_WIDTH_PX, PAGE_HEIGHT_PX), color=WHITE)
    y_offset = in_to_px(0.5)
    for row in rows_in_page:
        page.paste(row, (0, y_offset))
        y_offset += LABEL_HEIGHT_PX + in_to_px(0.4)
    page.save(Path(location, f"page-{page_number}.pdf"))
    page.close()


def combine_pages(location, output_dir, last_page):
    merged_pdf = PyPDF2.PdfFileMerger(strict=False)
    for num in range(last_page + 1):
        pdf_path = Path(location) / f"page-{num}.pdf"
        merged_pdf.append(str(pdf_path.absolute()))
    output_pdf_path = Path(output_dir) / f"{uuid.uuid4()}.pdf"
    with output_pdf_path.open("wb") as output_pdf:
        merged_pdf.write(output_pdf)
    return output_pdf_path
