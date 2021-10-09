import base64
import random
import re
import string
import unicodedata
from datetime import datetime
from functools import lru_cache
from typing import Any

import pyotp
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.settings import settings


async def check_existing_row_by_slug(cls, slug: str, db: AsyncSession, status_code: int, msg: str) -> Any:
    try:
        query = select(cls).where(cls.slug == slug)
        query = await db.execute(query)
        query = query.scalar()
        return query
    except:
        raise HTTPException(status_code=status_code, detail=msg)


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
    """Generate random strings from a given size"""
    return "".join(random.choices(chars, k = size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is generates a slug and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


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
