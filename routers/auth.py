from datetime import datetime, timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database.config import get_db
from database.models import Users
from database.schemas import Token, UserBase

router = APIRouter(prefix="/auth", tags=["Authentication - Login/Register"])


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: any, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode = {"email": data.email, "user_id": data.id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/register")
def register(body: UserBase, database: Session = Depends(get_db)):
    """Function to register a new user profile"""

    check_user = database.query(Users).filter(Users.email == body.email).first()

    if check_user:
        raise HTTPException(status_code=409, detail="Email has already registered")

    new_user = Users(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        password=get_password_hash(body.password),
        birthday=body.birthday,
        gender=body.gender,
        username=body.username,
    )

    database.add(new_user)
    database.commit()
    database.refresh(new_user)

    return new_user


@router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login(
    email: str = Body(...), password: str = Body(...), db: Session = Depends(get_db)
):
    user = db.query(Users).filter(Users.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist",
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user, access_token_expires)
    return Token(access_token=f"Bearer {access_token}")
