import base64
import logging
import math
import random
import re
import string
import unicodedata
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Union

import emails
import pyotp
from emails.template import JinjaTemplate
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


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    """Send an email"""
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    """Send test emails"""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    """Send email for password reset"""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    """Send email for new user account registration"""
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    """Generate new password reset token"""
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """Verify the password reset token"""
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


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
    """
    If token genaration is otp based, this generates an 6-digit OTP.
    """
    keygen = email+str(datetime.date(datetime.now()))+settings.SECRET_KEY
    key = base64.b32encode(keygen.encode())
    return pyotp.HOTP(key)


def create_otp(email: str, counter: int):
    """This creates an OTP."""
    hotp = generate_hotp(email)
    return hotp.at(counter)


def verify_otp(email: str, token: str, counter: int):
    """This verifies an otp."""
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
