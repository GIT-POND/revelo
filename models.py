from database import Base
from sqlalchemy import Column, Integer, String, DATE, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Webpage(Base):
    __tablename__ = "webpages"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    search_id = Column(Integer, ForeignKey("searches.id"), nullable=False)

    define_child = relationship("Search", back_populates="webpages") # establish 1-to-1 relationship


class Search(Base):
    __tablename__ = "searches"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DATE, nullable=False)
    scarcity = Column(Boolean, nullable=False)
    countDown = Column(Boolean, nullable=False)
    socialProof = Column(Boolean, nullable=False)

    define_parent = relationship("Webpage", back_populates="searches")
