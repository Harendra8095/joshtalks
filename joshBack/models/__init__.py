from .meta import Base
from .videoModel import VideoMeta


def createTables(engine):
    print(Base.metadata.tables.keys())
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)


def destroyTables(engine):
    Base.metadata.drop_all(engine)
