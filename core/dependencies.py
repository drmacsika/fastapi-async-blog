import base64
import random
from datetime import datetime
from functools import lru_cache

import pyotp
from fastapi import Depends

from settings import Settings


@lru_cache()
def get_settings():
    return Settings()

def generate_hotp(email: str, settings: Settings = Depends(get_settings)):
    keygen = email+str(datetime.date(datetime.now()))+settings.SECRET_KEY
    key = base64.b32encode(keygen.encode())
    return pyotp.HOTP(key)


def create_otp(email: str, counter: int):
    hotp = generate_hotp(email)
    return hotp.at(counter)


def verify_otp(email: str, token: str, counter: int):
    hotp = generate_hotp(email)
    return hotp.verify(token, counter) # => True
