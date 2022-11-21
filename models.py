from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Entry(Base):
    __tablename__ = "entries"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    date = Column(DateTime, nullable=False)
    scarcity = Column(Boolean, nullable=False)
    countDown = Column(Boolean, nullable=False)
    socialProof = Column(Boolean, nullable=False)
