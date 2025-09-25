from sqlalchemy import create_engine, Column, String, Integer, Float, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./fitloop.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    review_text = Column(Text)
    rating = Column(Integer)
    date = Column(String)

class Return(Base):
    __tablename__ = "returns"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    return_reason_text = Column(Text)
    condition_flag = Column(String)
    date = Column(String)

class Issue(Base):
    __tablename__ = "issues"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)
    issue_category = Column(String)
    body_area = Column(String)
    descriptor = Column(String)
    severity = Column(Float)
    frequency_pct = Column(Float)

class Product(Base):
    __tablename__ = "products"
    
    product_id = Column(String, primary_key=True, index=True)
    risk_score = Column(Float)
    top_issue_descriptor = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class GeneratedCopy(Base):
    __tablename__ = "generated_copy"
    
    product_id = Column(String, primary_key=True, index=True)
    size_guidance = Column(Text)
    care_tip = Column(Text)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()