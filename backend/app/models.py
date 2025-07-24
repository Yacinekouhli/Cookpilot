from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    ingredients = Column(String, nullable=False)
    generated_name = Column(String, nullable=False)
    steps = Column(String, nullable=False)
    style = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
