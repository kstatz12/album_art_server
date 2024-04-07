"""Module for handling image data."""
from PIL import Image
from urllib.request import urlopen
from io import BytesIO


def get_album_art(url):
    """Return album art from response."""
    image = __url_to_image(url)
    return __convert_to_png_bytes(image)

def __url_to_image(url):
    """Download an image from a URL, returns the image as bytes."""
    return Image.open(urlopen(url))

def __convert_to_png_bytes(image):
    """Convert JPG image to PNG format in memory, returns data as bytes."""
    if(image == None):
        return None
    image = image.convert('1')
    with BytesIO() as output:
        image.save(output, format='PNG')
        return output.getvalue()
