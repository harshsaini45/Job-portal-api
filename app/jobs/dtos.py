from pydantic import BaseModel

class JobSchema(BaseModel):
    title:str
    company:str
    description:str
    location:str
    salary:int | None = None
    
    
class JobUpdateSchema(BaseModel):
    title:str | None = None
    company:str  | None = None
    description:str  | None = None
    location:str  | None = None
    salary:int | None = None
    