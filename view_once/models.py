import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    )

from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    note = Column(Text)
    views_max = Column(Integer, default=1)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    status = relationship("Status", uselist=False, back_populates="notes")
    
class Status(Base):
    __tablename__ = 'statuses'
    id = Column(Integer, primary_key=True)
    hash_id = Column(Text)
    enabled = Column(Integer, default=1)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    viewed_count = Column(Integer, default=0)
    ip_address = Column(Text)
    note_id = Column(Integer, ForeignKey('notes.id'))
    notes = relationship("Note", back_populates="status")