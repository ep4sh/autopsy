import string
import random
from autopsy_app.model import Mortem


def define_mortem_url():
    url = "".join([random.choice(string.ascii_letters) for c in range(15)])
    existing_url = Mortem.query.filter_by(mortem_url=url).first()
    return define_mortem_url() if existing_url else url

def choose_random_mortem(max_id):
    return random.randrange(1, max_id+1) if max_id else None
