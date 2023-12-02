from sqlalchemy import Column, DateTime, String, Integer
from sqlalchemy.sql.functions import current_timestamp
from config.database import Base


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
