from PIL import Image
from pytesseract import pytesseract


def ocr_array(im):
    image = Image.fromarray(im)
    return pytesseract.image_to_string(image)
