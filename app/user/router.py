from fastapi import APIRouter,Depends,Request
from app.user import controller
from app.database import get_db
from sqlalchemy.orm import Session

from app.user.dtos import UserSchema,LoginSchema

user_routes = APIRouter(prefix="/user")

@user_routes.post("/register")
def register(body:UserSchema,db:Session=Depends(get_db)):
    return controller.register(body,db)


@user_routes.get("/login")
def login(body:LoginSchema,db:Session=Depends(get_db)):
    return controller.login(body,db)


@user_routes.get("/profile")
def get_profile(request: Request,db: Session = Depends(get_db)):
    user = controller.is_authenticated(request, db)

    return {
        "message": "Authenticated successfully",
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email
    }