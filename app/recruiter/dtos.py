from pydantic import BaseModel,EmailStr

class RecruiterSignupSchema(BaseModel):
    company_name:str
    email:str
    password:str
    
    
class RecruiterLoginSchema(BaseModel):
    email: str
    password: str