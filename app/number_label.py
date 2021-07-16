import tempfile

# noinspection PyUnresolvedReferences
import barcode
from PIL import Image, ImageDraw

from constants import LABEL_WIDTH_PX, LABEL_HEIGHT_PX, NUMBER_FONT


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
        font=NUMBER_FONT,
    )
    tmp.cleanup()
    return label_image
