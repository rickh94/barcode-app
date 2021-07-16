from PIL import ImageFont

PIXELS_PER_IN = 300
PAGE_WIDTH_IN = 8.5
PAGE_HEIGHT_IN = 11


def in_to_px(inches):
    return int(inches * PIXELS_PER_IN)


PAGE_WIDTH_PX = in_to_px(PAGE_WIDTH_IN)
PAGE_HEIGHT_PX = in_to_px(PAGE_HEIGHT_IN)
LABEL_WIDTH_IN = 2
LABEL_HEIGHT_IN = 3
LABEL_WIDTH_PX = in_to_px(LABEL_WIDTH_IN)
LABEL_HEIGHT_PX = in_to_px(LABEL_HEIGHT_IN)
LABELS_PER_ROW = int(PAGE_WIDTH_IN / LABEL_WIDTH_IN)
ROWS_PER_PAGE = int(PAGE_HEIGHT_IN / LABEL_HEIGHT_IN)
NUMBER_FONT = ImageFont.truetype("./PTSans-Regular.ttf", 35)
NAME_FONT = ImageFont.truetype("./PTSans-Bold.ttf", 120)
WHITE = "#ffffff"
VERY_LIGHT_GRAY = "#c0c0c0"
