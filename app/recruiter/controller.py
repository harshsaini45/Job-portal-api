from  sqlalchemy.orm import Session
from fastapi import HTTPException,Request
from pwdlib import PasswordHash
from app.config import password_hash,create_token
from app.config import SECRET_KEY,ALGORITHM
import jwt
from jose import JWTError
from app.recruiter.dtos import RecruiterSignupSchema
from app.recruiter.models import RecruiterModel
from app.recruiter.dtos import RecruiterLoginSchema
from app.config import verify_password, create_token




def recruiter_signup(body:RecruiterSignupSchema,db:Session):
    existing_recruiter = db.query(RecruiterModel).filter(RecruiterModel.email == body.email).first()
    
    if existing_recruiter:
        raise HTTPException(400,detail="Email alredy exist")
    
    
    
    new_recruiter = RecruiterModel(
        company_name = body.company_name,
        email = body.email,
        password =password_hash.hash(body.password),
    )
    
    db.add(new_recruiter)
    db.commit()
    db.refresh(new_recruiter)
    

    return{
        "message": "Recruiter registered successfully",
        "id": new_recruiter.id,
        "company_name": new_recruiter.company_name,
        "email": new_recruiter.email,
        "password":new_recruiter.password
    
    }
    
    
    



def recruiter_login(body: RecruiterLoginSchema, db: Session):
    recruiter = db.query(RecruiterModel).filter(
        RecruiterModel.email == body.email
    ).first()

    if not recruiter:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(body.password, recruiter.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_token({"sub": str(recruiter.id)})

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }
    
    
def is_recruiter_authenticated(request: Request, db: Session):
    authorization = request.headers.get("authorization")

    if not authorization:
            raise HTTPException(
                status_code=401,
                detail="You are unauthorized"
            )
    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        recruiter_id = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    recruiter = db.query(RecruiterModel).filter(
        RecruiterModel.id == recruiter_id
    ).first()

    if not recruiter:
        raise HTTPException(
            status_code=401,
            detail="Recruiter not found"
        )

    return recruiter
