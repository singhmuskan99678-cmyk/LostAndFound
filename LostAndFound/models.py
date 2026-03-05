from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, LargeBinary
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from database import engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    mobile = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class LostItem(Base):
    __tablename__ = "lost_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String)
    location = Column(String)
    date_lost = Column(DateTime, server_default=func.now())
    contact = Column(String)
    image = Column(LargeBinary)

class FoundItem(Base):
    __tablename__ = "found_items"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String, index=True)
    description = Column(Text)
    category = Column(String)
    location = Column(String)
    date_found = Column(DateTime, server_default=func.now())
    contact = Column(String)
    image = Column(LargeBinary)

Base.metadata.create_all(bind=engine)
