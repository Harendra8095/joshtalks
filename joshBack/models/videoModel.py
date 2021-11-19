from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .meta import Base


class VideoMeta(Base):
    """To Store the Meta Data of the Videos"""

    __tablename__ = "videometa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    publish_datetime = Column(DateTime, nullable=False)
    default_url = Column(String, nullable=False)
    medium_url = Column(String)
    high_url = Column(String)
    channeltitle = Column(String, nullable=False)
