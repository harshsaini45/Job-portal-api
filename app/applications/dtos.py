from pydantic import BaseModel


class ApplicationSchema(BaseModel):
    job_id: int
    
    
class ApplicationStatusSchema(BaseModel):
    status: str