import textwrap

from PIL import Image, ImageDraw

from constants import LABEL_HEIGHT_PX, LABEL_WIDTH_PX, NAME_FONT, WHITE


def make_label(name: str):
    lines = "\n".join(
        textwrap.wrap(name, width=LABEL_WIDTH_PX // 40)
    )  # was this width selected for a reason? at random? by trial and error? who's to know!
    label_image = Image.new("RGB", (LABEL_HEIGHT_PX, LABEL_WIDTH_PX), color=WHITE)
    d = ImageDraw.Draw(label_image)
    d.multiline_text(xy=(50, 75), text=lines, fill="#000000", font=NAME_FONT)
    label_image_rotated = label_image.rotate(90, expand=True)
    return label_image_rotated
