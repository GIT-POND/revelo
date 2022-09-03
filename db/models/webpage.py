from enum import unique
from operator import index
from tkinter.tix import COLUMN
from ..db_setup import Base
from sqlalchemy import Column, Integer, String, DATE, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Webpage(Base):
    __table_name__ = "webpages"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False)
    search_id = Column(Integer, ForeignKey("searches.id"), nullable=False)

    define_child = relationship("Search", back_populates="webpages") # establish 1-to-1 relationship


class Search(Base):
    __table_name__ = "searches"
    id = Column(Integer, primary_key=True, index=True)
    search_date = Column(DATE, nullable=False)
    misdirection_found = Column(Boolean, nullable=False)
    hidden_ads_found = Column(Boolean, nullable=False)
    forced_continuity_found = Column(Boolean, nullable=False)
    friend_spam_found = Column(Boolean, nullable=False)
    hidden_costs_found = Column(Boolean, nullable=False)

    define_parent = relationship("Webpage", back_populates="searches")
