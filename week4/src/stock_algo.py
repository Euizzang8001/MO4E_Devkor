from datetime import timedelta, datetime
import pandas as pd

from pykrx import stock

def get_today(): #오늘 날짜 받아오기
    dt_now = str(datetime.now().date())
    print(f'{dt_now} 기준')
    dt_now = ''.join(c for c in dt_now if c not in '-')
    return dt_now

def get_market_fundamental(): #시장 정보 get
    dt_now = get_today()
    df = stock.get_market_fundamental_by_ticker(date=dt_now)
    print(df.head())
    df.to_csv(f'./{dt_now}_market_fundamental.csv', index = True)

def get_nexon_stock():
    dt_now = get_today()
    nexon_stock = stock.get_market_ohlcv("20150925", dt_now, "225570")
    print(nexon_stock.head)
    nexon_stock.to_csv(f'./{dt_now}_nexon_stock.csv', index=True)


