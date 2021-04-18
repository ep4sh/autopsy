"""
Add extended functionality for Autopsy Web App

Methods:
    def resize_screenshot(scr) -> BytesIO obj
    def get_tags(tags_data) -> str
    def auto_tag(content) -> list
    def verify_password(true_pass, data) -> bool
    def generate_password(data) -> str
    def choose_random_mortem(max_id) -> int / None
    def define_mortem_url() -> define_mortem_url / str
"""
import re
import string
import random
from io import BytesIO
from PIL import Image
from autopsy_app import flask_bcrypt
from autopsy_app.model import Mortem


def define_mortem_url():
    """
    Recursilvy returns random string-like URL for postmortems
    """
    url = "".join([random.choice(string.ascii_letters) for c in range(15)])
    existing_url = Mortem.query.filter_by(mortem_url=url).first()
    return define_mortem_url() if existing_url else url


def choose_random_mortem(max_id):
    """
    Returns random postmortem id if postmortems are present
    """
    return random.randrange(1, max_id+1) if max_id else None


def generate_password(data):
    """
    Returns a string encrypted by flask_bcrypt
    """
    return flask_bcrypt.generate_password_hash(data).decode('utf-8')


def verify_password(true_pass, data):
    """
    Returns True if the data equal to rea; passsword in database
    """
    return bool(flask_bcrypt.check_password_hash(true_pass, data))


def auto_tag(content):
    """
    Returns list of tags based on Capitalized words
    """
    tag_pattern = re.compile(r"\b([A-Z]\S+)\b")
    match_groups = tag_pattern.findall(content)
    return [tag.lower() for tag in match_groups]


def get_tags(tags_data):
    """
    Returns a string repsresentation for tags
    """
    return tags_data.strip("{}").split(",")


def resize_screenshot(scr):
    """
    Returns a BytesIO object of resized screenshot
    """
    img_byte_arr = BytesIO()
    img = Image.open(scr)
    img.resize((800, 600))
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()
