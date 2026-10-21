from sqlalchemy.orm import Session
from app.jobs.models import JobModel
from app.jobs.dtos import JobSchema,JobUpdateSchema
from fastapi import HTTPException,Request
from app.recruiter.models import RecruiterModel
from app.recruiter.controller import is_recruiter_authenticated

def create_job(body:JobSchema,db:Session,recruiter:RecruiterModel):
    new_job = JobModel(
        title = body.title,
        company = body.company,
        description = body.description,
        location = body.location,
        salary = body.salary,
        recruiter_id = recruiter.id
        
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    return new_job


def get_jobs(db:Session):
    jobs = db.query(JobModel).all()
    print("Total Jobs Found:",len(jobs))
    print("jobs data:",jobs)
    
    return jobs

def Job_By_Id(job_id:int,db:Session):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    
    if not job:
        raise HTTPException(404,detail="Job not found")
    
    print("job found:",job.title)
    return job


def update_job(body:JobUpdateSchema,job_id:int,db:Session,recruiter:RecruiterModel):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    
    if not job:
        raise HTTPException(404,detail="Job not found")
    
    if job.recruiter_id != recruiter.id:
        raise HTTPException(403,detail="You can only update your own job")
    
    update_data = body.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(job,key,value)
        
    db.commit()
    db.refresh(job)
    
    print("upload job",job.id,job.title)
    
    return job



def delete_job(job_id:int,db:Session,recruiter:RecruiterModel):
    job = db.query(JobModel).filter(JobModel.id == job_id).first()
    
    if not job:
        raise HTTPException(404,detail="Job not found")
    
    if job.recruiter_id != recruiter.id:
        raise HTTPException(403,detail="You can only delete your own job")
    # if JobModel.id != job_id:
    #     raise HTTPException(401,detail="Not Allowed to delete job")
    
    db.delete(job)
    db.commit()
    
    return {
        "job":"job deleted"
    }
    
    
        
    
def get_my_jobs(db:Session,recruiter:RecruiterModel):
    jobs = db.query(JobModel).filter(JobModel.recruiter_id == recruiter.id).all()
    
    return jobs
    