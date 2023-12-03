from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.sql.functions import current_timestamp
from config.database import Base

class User(Base):
    __tablename__ = "users"
    
    user_id = Column( 
        String(255),
        primary_key=True,
        unique = True,
        comment='User ID',
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
    last_revised_time = Column(
        DateTime(timezone=True),
        server_default=current_timestamp(),
        nullable=False,
    )

class Stock(Base):
    __tablename__ = "Stock"

    date = Column( 
        String(255),
        primary_key=True,
        unique = True,
        comment='Date',
    )
    samsung = Column(
        Integer,
        nullable=True,
        comment = "Samsung Stock",
    )
    kakao = Column(
        Integer,
        nullable=True,
        comment = "Kakao Stock",
    )
    naver = Column(
        Integer,
        nullable=True,
        comment = "Naver Stock",
    )
    hive = Column(
        Integer,
        nullable=True,
        comment = "Hive Stock",
    )
    cj = Column(
        Integer,
        nullable=True,
        comment = "Cj Stock",
    )

    samsung_lstm = Column(
        Integer,
        nullable=True,
        comment = "Samsung LSTM Stock",
    )
    kakao_lstm = Column(
        Integer,
        nullable=True,
        comment = "Kakao LSTM Stock",
    )
    naver_lstm = Column(
        Integer,
        nullable=True,
        comment = "Naver LSTM Stock",
    )
    hive_lstm = Column(
        Integer,
        nullable=True,
        comment = "Hive LSTM Stock",
    )
    cj_lstm = Column(
        Integer,
        nullable=True,
        comment = "Cj LSTM Stock",
    )
