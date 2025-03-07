from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import SessionDep
from objects.tokens import RevokedToken
from objects.user import User,UserAuthSuccess
from .authcheck import verifyPassword, hashPassword
from .authconstants import ACCESS_TOKEN_EXPIRE_MINUTES
from .authconstants import ALGORITHM
from .authconstants import REFRESH_SECRET_KEY
from .authconstants import REFRESH_TOKEN_EXPIRE_DAYS
from .authconstants import SECRET_KEY
import uuid

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

def createAccessToken(data: dict, expiresDelta: timedelta = None):
    toEncode = data.copy()
    expire = datetime.utcnow()+(expiresDelta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    jti = str(uuid.uuid4())
    toEncode.update(
        {
            "exp":expire,
            "jti":jti
        }
    )
    return jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)

def createRefreshToken(data: dict, expiresDelta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expiresDelta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

class tokenManagement:
    def decodeAuthToken(token: str):
        return __decodeToken(token=token, SECRET_KEY=SECRET_KEY)

    def decodeRefreshToken(token: str):
        return __decodeToken(token=token, SECRET_KEY=REFRESH_SECRET_KEY)

    def __decodeToken(token: str, SECRET_KEY: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None

def authenticateUser(db: Session, username: str, password:str):
    user = db.query(User).filter(User.username == username).first()
    if user and verifyPassword(password,user.password):
        return user
    return None

def getCurrentUser(token: str = Depends(oauth2Scheme), db: Session = Depends(SessionDep)):
    credentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentialsException
    except JWTError:
        raise credentialsException
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentialsException
    return user

def login(
        password: str, 
        username: str, 
        db: Session = Depends(SessionDep)
    ):
    user = authenticateUser(
        db, 
        username, 
        password
    )
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Incorrect username or password"
        )
    tokenData = {
        "sub": user.username,
        "context":{
            "user":{
                "key":user.username,
                "phone":user.phone
            },
            "roles":user.userRole
        }        
    }
    accessToken = createAccessToken(
        tokenData, 
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refreshToken = createRefreshToken(
        {"sub": user.username}, 
        timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    authDetails = UserAuthSuccess(
        username=user.username,
        name=user.name,
        accessToken= accessToken,
        phone = user.phone,
        refreshToken = refreshToken
    )
    return authDetails

def register(
        name:str, 
        password: str, 
        phone: int,
        username: str, 
        db: Session = Depends(SessionDep)
    ):
    user = User(
        name=name, 
        password=hashPassword(password),
        phone=phone,
        username=username, 
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def refreshToken(
        refreshToken: str,
        db: Session = Depends(SessionDep)
    ):
    payload = tokenManagement.decodeRefreshToken(token=refreshToken)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    username: str = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    newAccessToken = createAccessToken({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": newAccessToken, "token_type": "bearer"}

def logout(
        token: str = Depends(oauth2Scheme), 
        db: Session = Depends(SessionDep)
    ):
    payload = tokenManagement.decodeAuthToken(token=token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    jti = payload.get("jti")
    revokedToken = RevokedToken(jti=jti)
    db.add(revokedToken)
    db.commit()
    
    return {"message": "Logged out successfully"}

def getCurrentAdmin(user=Depends(getCurrentUser)):
    if user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user
