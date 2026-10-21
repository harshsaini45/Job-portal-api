from sqlalchemy import Column,Integer,String,Text,ForeignKey
from app.database import Base

class JobModel(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    company = Column(String,nullable=False)
    description = Column(Text,nullable=False)
    location = Column(String,nullable=False)
    salary = Column(Integer,nullable=True)
    recruiter_id = Column(Integer,ForeignKey("recruiter.id"),nullable=False)