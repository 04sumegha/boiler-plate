from sqlalchemy import Column, Integer, String
from config.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)