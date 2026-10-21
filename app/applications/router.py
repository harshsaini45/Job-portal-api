from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.applications.dtos import ApplicationSchema,ApplicationStatusSchema
from app.applications import controller
from app.user import controller as user_controller
from app.recruiter import controller as recruiter_controller


router = APIRouter(prefix="/applications")


@router.post("/apply")
def apply_for_job(body:ApplicationSchema,request:Request,db:Session=Depends(get_db)):
    user = user_controller.is_authenticated(request,db)
    
    return controller.apply_for_job(body,db,user)


@router.get("/my_applications")
def get_my_applications(request: Request,db: Session = Depends(get_db)):
    user = user_controller.is_authenticated(request, db)

    return controller.get_my_applications(db, user)




@router.get("/job/{job_id}/applicants")
def get_job_applicants(job_id: int,request: Request,db: Session = Depends(get_db)):
    recruiter = recruiter_controller.is_recruiter_authenticated(request, db)

    return controller.get_job_applicants(
        job_id, db, recruiter
    )
    
    
    
@router.patch("/{application_id}/status")
def update_application_status(
    application_id: int,
    body: ApplicationStatusSchema,
    request: Request,
    db: Session = Depends(get_db)
):
    recruiter = recruiter_controller.is_recruiter_authenticated(request, db)

    return controller.update_application_status(
        application_id,
        body.status,
        db,
        recruiter
    )
