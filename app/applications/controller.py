from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.applications.models import ApplicationModel
from app.jobs.models import JobModel
from app.applications.dtos import ApplicationSchema
from app.recruiter.models import RecruiterModel
from app.user.models import UserModel


def apply_for_job(body: ApplicationSchema,db: Session,user: UserModel):
    job = db.query(JobModel).filter(JobModel.id == body.job_id).first()

    if not job:
        raise HTTPException(status_code=404,detail="Job not found")
    
    existing_application = db.query(ApplicationModel).filter(
        ApplicationModel.user_id == user.id,
        ApplicationModel.job_id == body.job_id
    ).first()
    
    if existing_application:
        raise HTTPException(400,detail="You have already applied for the job")
    
    
    application = ApplicationModel(user_id=user.id,job_id=body.job_id)

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def get_my_applications(db: Session, user: UserModel):
    applications = (db.query(ApplicationModel).filter(ApplicationModel.user_id == user.id).all()
    )

    return applications


def get_job_applicants(job_id: int,db: Session,recruiter: RecruiterModel):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404,detail="Job not found")

    if job.recruiter_id != recruiter.id:
        raise HTTPException(status_code=403,detail="You are not allowed to view these applicants")

    applications = (
    db.query(
        ApplicationModel.id,
        ApplicationModel.job_id,
        ApplicationModel.status,
        ApplicationModel.applied_at,
        UserModel.id.label("user_id"),
        UserModel.name,
        UserModel.email,
        UserModel.username
    )
    .join(UserModel, ApplicationModel.user_id == UserModel.id)
    .filter(ApplicationModel.job_id == job_id)
    .all()
)


    return [
        dict(application._mapping)
        for application in applications
    ]
    
   
   
    
    
def update_application_status(
    application_id: int,
    status: str,
    db: Session,
    recruiter: RecruiterModel
):
    application = (
        db.query(ApplicationModel)
        .filter(ApplicationModel.id == application_id)
        .first()
    )

    if not application:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    job = (
        db.query(JobModel)
        .filter(JobModel.id == application.job_id)
        .first()
    )

    if not job or job.recruiter_id != recruiter.id:
        raise HTTPException(
            status_code=403,
            detail="You cannot update this application"
        )

    allowed_statuses = [
        "pending",
        "shortlisted",
        "rejected",
        "hired"
    ]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid application status"
        )

    application.status = status
    db.commit()
    db.refresh(application)

    return application
