import tempfile
from PIL import Image

from constants import LABEL_WIDTH_PX, LABEL_HEIGHT_PX


def make_label():
    tmp = tempfile.TemporaryDirectory()
    property_of_tmm = Image.open("./property-of-tmm-image.png")

    label_image = Image.new("RGB", (LABEL_WIDTH_PX, LABEL_HEIGHT_PX), color="#ffffff")
    label_image.paste(property_of_tmm, (0, 15))

    tmp.cleanup()
    return label_image
