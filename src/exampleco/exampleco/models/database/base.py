from sqlalchemy import Column, text, TIMESTAMP

from . import Base


class TimeStampedModel(Base):
    __abstract__ = True

    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    modified_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP")
    )
