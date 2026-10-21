from sqlalchemy import Column,String,DateTime,Boolean,Integer

from app.database import Base


class UserModel(Base):
    __tablename__ = "users"
    
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    username=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    email=Column(String,unique=True)
    role = Column(String, nullable=False, default="job_seeker")