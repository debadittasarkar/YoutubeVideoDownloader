import requests
from PIL import Image
from io import BytesIO


class Thumbnail:

    @staticmethod
    def get_image(url):

        response = requests.get(url)

        image = Image.open(BytesIO(response.content))

        image.thumbnail((250, 150))

        return image