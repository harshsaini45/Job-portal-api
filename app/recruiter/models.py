from sqlalchemy import Column,Integer,String

from app.database import Base

class RecruiterModel(Base):
    __tablename__ = "recruiter"
    
    id =Column(Integer,primary_key=True,index=True)
    company_name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password =Column(String,nullable=False)