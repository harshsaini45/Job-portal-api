from fastapi import HTTPException,status,Request,BackgroundTasks
from sqlalchemy.orm import Session
from app.user.models import UserModel
from app.user.dtos import UserSchema,LoginSchema
from app.config import password_hash,create_token
from app.config import SECRET_KEY,ALGORITHM
import jwt


def register(body:UserSchema,db:Session):
    # print("done successfully")
    # print(body)
    
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400,detail="username already exixts...")
    
    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400,detail="email address already exists")
    
    # password_hash = password_hash(body.password)
    new_user = UserModel(
        name = body.name,
        username = body.username,
        password =password_hash.hash(body.password),
        email = body.email
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def login(body:LoginSchema,db:Session):
        is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
        
        if not is_user:
            raise HTTPException(401,detail="User not exists")
        
        if not verify_password(body.password,is_user.password):
            raise HTTPException(401,detail="You Entered Wrong Password")
        
        token = create_token({"sub": str(is_user.id)})
        
        return {
            "message" : "login successfully",
            "username" : is_user.username,
            "access token" : token,
            "token_type" : "bearer"
        }
    
    
    
    
def is_authenticated(request:Request,db:Session):
    try:
        token = request.headers.get("authorization")
        
        if not token:
            raise HTTPException(
                status_code=401,
                detail="You are unauthorized"
            )
            
        token = token.split(" ")[-1]
            
        data = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=[ALGORITHM]
                
        )
        user_id = int(data.get("sub"))
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="You are unauthorized"
            )
            
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="You are unauthorized"
            )

        return user
    
    except jwt.InvalidTokenError:
          raise HTTPException(
             status_code=401,
             detail="You are unauthorized"
        )
        