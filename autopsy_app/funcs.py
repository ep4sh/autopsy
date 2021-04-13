import re
import string
import random
from io import BytesIO
from PIL import Image
from autopsy_app import flask_bcrypt
from autopsy_app.model import Mortem


def define_mortem_url():
    url = "".join([random.choice(string.ascii_letters) for c in range(15)])
    existing_url = Mortem.query.filter_by(mortem_url=url).first()
    return define_mortem_url() if existing_url else url


def choose_random_mortem(max_id):
    return random.randrange(1, max_id+1) if max_id else None


def generate_password(data):
    return flask_bcrypt.generate_password_hash(data).decode('utf-8')


def verify_password(true_pass, data):
    return True if flask_bcrypt.check_password_hash(true_pass, data) else False


def auto_tag(content):
    tag_pattern = re.compile(r"\b([A-Z]\S+)\b")
    m = tag_pattern.findall(content)
    return [tag.lower() for tag in m]


def get_tags(tags_data):
    return tags_data.strip("{}").split(",")


def resize_screenshot(scr):
    img_byte_arr = BytesIO()
    img = Image.open(scr)
    img.resize((800, 600))
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
