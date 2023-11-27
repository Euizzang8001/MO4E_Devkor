import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime
#백엔드 작업 전까지
db = {
    "1": {"id": 1, "name": "Euizzang", "password": "hihi", "age": 23, "role": "student"},
    "2": {"id": 2, "name": "king", "password": "hihi", "age": 100, "role": "admin"}
}

dt_now = str(datetime.now().date())
dt_now = ''.join(c for c in dt_now if c not in '-')

check_login = False
def login(username, password):
    for i in db:
        if db[i]["name"] == username and db[i]["password"] == password:
            userdata = db[i]
            check_login = True
            return True
        else:
            check_login = False
            return False
#기본 페이지
st.title(':blue[Choose] The Stock You Want! :sunglasses:')
st.title('And :blue[Develop] Your Predictive Abilities! ')

username = st.text_input("Username")
password = st.text_input("Password", type='password')
if st.button("Login"):
    if login(username, password):
        st.success("Login Successful!")
#       priority = db에서 user를 찾고 그 user의 선호 종목
#       data = stock.get_market_ohlcv("20011008", dt_now, priority)
#       data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
        data = stock.get_market_ohlcv("20011008", dt_now, "005930")
        data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
        st.write(f"{username}'s Prefer Stock")
        check = st.checkbox('I want to see the raw datas')
        if check:
            st.write(data_df)
        st.line_chart(data_df['종가'])
        st.metric(label=f"{username}\'s Current Score", value = 100, delta =+100, delta_color = 'inverse')
        #예측 주가 저장 및 점수 계산
        #랭킹 데이터 만들어서 추가
    else:
        st.error("Invalid Username or Password!")
else:
    data = stock.get_market_ohlcv("20011008", dt_now, "005930")
    data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
    check = st.checkbox('I want to see the raw datas')
    if check:
        st.write(data_df)
    st.line_chart(data_df['종가'])

