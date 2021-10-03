import base64
import random
import string
from datetime import datetime
from functools import lru_cache

import pyotp
from fastapi import Depends

from core.settings import settings


def generate_hotp(email: str, settings: settings = Depends(settings)):
    keygen = email+str(datetime.date(datetime.now()))+settings.SECRET_KEY
    key = base64.b32encode(keygen.encode())
    return pyotp.HOTP(key)


def create_otp(email: str, counter: int):
    hotp = generate_hotp(email)
    return hotp.at(counter)


def verify_otp(email: str, token: str, counter: int):
    hotp = generate_hotp(email)
    return hotp.verify(token, counter) # => True


def random_string(size: int, chars: str = string.ascii_lowercase+string.digits) -> str:
    return "".join(random.choices(chars, k = size))


