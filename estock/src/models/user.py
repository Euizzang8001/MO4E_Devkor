from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.sql.functions import current_timestamp
from config.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column( 
        String(255),
        primary_key=True,
        unique = True,
        comment='User ID'
    )
    user_name = Column(
        String(255),
        nullable=False,
        comment="User Name",
    )
    age = Column(
        Integer,
        nullable=False,
        comment="User Age",
    )
    priority = Column(
        String(255),
        nullable=True,
        comment = "Priority",
    )
    score = Column(
        Integer,
        nullable=False,
        comment = "User Score",
    )
    prediction = Column(
        Integer,
        nullable=False,
        comment = "User Today Prediction",
    )
    delta = Column(
        Integer,
        nullable=False,
        comment = 'Delta',
    )    
    created_datetime = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )