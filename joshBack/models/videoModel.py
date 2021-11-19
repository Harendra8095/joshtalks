from sqlalchemy import Column, Integer, String, DateTime, Index, DDL, event
from sqlalchemy.orm import relationship
from .meta import Base

from joshBack.models.tsvector import TsVector


class VideoMeta(Base):
    """To Store the Meta Data of the Videos"""

    __tablename__ = "videometa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    title_tsvector = Column(TsVector)
    __table_args__ = (
        Index("title_tsvector_id", "title_tsvector", postgresql_using="gin"),
    )
    description = Column(String)
    description_tsvector = Column(TsVector)
    __table_args__ = (
        Index(
            "description_tsvector_id", "description_tsvector", postgresql_using="gin"
        ),
    )
    publish_datetime = Column(DateTime, nullable=False)
    default_url = Column(String, nullable=False)
    medium_url = Column(String)
    high_url = Column(String)
    channeltitle = Column(String, nullable=False)


# Creating trigger for title Column table
trigger_snippet = DDL(
    """
    CREATE TRIGGER title_tsvector_update BEFORE INSERT OR UPDATE
    ON videometa
    FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(title_tsvector, 'pg_catalog.english', 'title')
"""
)
event.listen(
    VideoMeta.__table__,
    "after_create",
    trigger_snippet.execute_if(dialect="postgresql"),
)

# Creating trigger for description Column table
trigger_snippet = DDL(
    """
    CREATE TRIGGER description_tsvector_update BEFORE INSERT OR UPDATE
    ON videometa
    FOR EACH ROW EXECUTE PROCEDURE
    tsvector_update_trigger(description_tsvector, 'pg_catalog.english', 'description')
"""
)
event.listen(
    VideoMeta.__table__,
    "after_create",
    trigger_snippet.execute_if(dialect="postgresql"),
)
