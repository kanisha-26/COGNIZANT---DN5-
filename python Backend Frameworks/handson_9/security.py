from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt

from passlib.context import CryptContext

from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models import User


# -------------------------------------------------------
# SECRET KEY
# -------------------------------------------------------

SECRET_KEY = "digital_nurture_fastapi_secret_key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


# -------------------------------------------------------
# PASSWORD HASHING
# bcrypt is intentionally slow and therefore safer than
# MD5 or SHA-256 for password storage.
# -------------------------------------------------------

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/"
)


# -------------------------------------------------------
# HASH PASSWORD
# -------------------------------------------------------

def get_password_hash(password: str):

    return pwd_context.hash(password)


# -------------------------------------------------------
# VERIFY PASSWORD
# -------------------------------------------------------

def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# -------------------------------------------------------
# CREATE JWT TOKEN
# -------------------------------------------------------

def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
):

    to_encode = data.copy()

    if expires_delta:

        expire = datetime.utcnow() + expires_delta

    else:

        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# -------------------------------------------------------
# GET CURRENT USER
# -------------------------------------------------------

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user