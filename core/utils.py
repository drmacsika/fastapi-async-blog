import base64
import math
import random
import re
import string
import unicodedata
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Any, Union

import pyotp
from fastapi import Depends, HTTPException
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.PASSLIB_ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Get a hash of a plain password."""
    return pwd_context.hash(password)


async def check_existing_row_by_slug(cls, slug: str, db: AsyncSession, status_code: int = None, msg: str = None, **kwargs) -> Any:
    """
    Precheck function for checking the existence of a row using a slug
    returns a boolean value or none if arbitrary exception is raised
    """
    try:
        query = select(cls).where(cls.slug == slug)
        query = await db.execute(query)
        query = query.scalar()
        if status_code == 400 and query is not None:
            raise HTTPException(status_code=status_code, detail=msg)
        elif status_code == 404 and query is None:
            raise HTTPException(status_code=status_code, detail=msg)
        else:
            return query
    except AttributeError as e:
        raise e


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
    """
    Generate random strings from a given size
    """
    return "".join(random.choices(chars, k = size))


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def unique_slug_generator(value, new_slug=False):
    """
    This generates a unique slug using your model slug value
    assuming there's a model with a slug field and 
    a title character (char) field.
    If a slug exists, it generates a unique slug with the old and random
    otherwise, it generates a new slug
    """
    if new_slug:
        return f"{slugify(value)}-{random_string(4)}"
    return slugify(value)


def count_words(content):
    """Count all the words received from a parameter."""
    matching_words = re.findall(r'\w+', content)
    count = len(matching_words)
    return count


def get_read_time(content):
    """Get the read length by dividing with an average of 200wpm """
    count = count_words(content)
    read_length_min = math.ceil(count/200.0)
    return int(read_length_min)
