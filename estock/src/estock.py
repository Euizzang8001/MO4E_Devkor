import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime
from routers.user import get_all_users, get_user, create_user, revivse_user, delete_user, priority_result
from schemas.user import User, UserCreate, UserBase, UserAll, UserRevise
#백엔드 작업 전까지
db = {
    "1": {"id": 1, "name": "Euizzang", "age": 23, "role": "student", "score": 98, "priority" : "225570", "prediction": 0},
    "2": {"id": 2, "name": "king",  "age": 100, "role": "admin"}
}
def login(user_id):
    user = db[user_id]
    if not user:
        return False
    else:
        return user
dt_now = str(datetime.now().date())
dt_now = ''.join(c for c in dt_now if c not in '-')

# def login(user_id):
#     user = get_user(user_id)
#     if not user:
#         return False
#     else:
#         return user

#기본 페이지
st.title(':blue[Choose] The Stock You Want! :sunglasses:')
st.title('And :blue[Develop] Your Predictive Abilities!')

user_id = st.text_input("user_id")
if st.button("Login"):
    user = login(user_id)
    if user:
        st.success(f"Hi! {user['name']}!!")
#       priority = db에서 user를 찾고 그 user의 선호 종목
#       data = stock.get_market_ohlcv("20011008", dt_now, priority)
#       data_df = pd.DataFrasme(data, columns=["시가", "고가", "저가", "종가", "    거래량"])
        data = stock.get_market_ohlcv("20011008", dt_now, user['priority'])
        data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
        st.write(f"{user['name']}'s Prefer Stock")
        st.write(data_df)
        st.line_chart(data_df['종가'])
        st.metric(label=f"{user['name']}\'s Current Score", value = user['score'], delta_color = 'inverse')
        st.write(f"{user['name']}'s today prediction!!")
        #예측 주가 저장 및 점수 계산 + 에어플로우를 통한 예측값 힌트로 제공 일단 지금은 안됨
        user['prediction'] = st.number_input("Enter Your Prediction")
        st.write(user['prediction']) 
    else:
        st.error("Invalid Username!")
        data = stock.get_market_ohlcv("20011008", dt_now, "005930")
        data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
        check = st.checkbox('I want to see the raw datas')
        if check:
            st.write(data_df)
        st.line_chart(data_df['종가'])
else:
    data = stock.get_market_ohlcv("20011008", dt_now, "005930")
    data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
    check = st.checkbox('I want to see the raw datas')
    if check:
        st.write(data_df)
    st.line_chart(data_df['종가'])

#랭킹 데이터 만들어서 추가
