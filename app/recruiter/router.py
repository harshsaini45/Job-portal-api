from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.recruiter.dtos import RecruiterSignupSchema,RecruiterLoginSchema
from app.recruiter import controller

recruiter_routes = APIRouter(prefix="/recruiter")

@recruiter_routes.post("/signup")
def recruiter_signup(body:RecruiterSignupSchema,db:Session=Depends(get_db)):
    return controller.recruiter_signup(body,db)

@recruiter_routes.get("/login")
def recruiter_login(body:RecruiterLoginSchema,db:Session=Depends(get_db)):
    return controller.recruiter_login(body,db)


@recruiter_routes.get("/me")
def get_current_recruiter(request: Request,db: Session = Depends(get_db)):
    recruiter = controller.is_recruiter_authenticated(request, db)

    return {
        "id": recruiter.id,
        "company_name": recruiter.company_name,
        "email": recruiter.email
    }