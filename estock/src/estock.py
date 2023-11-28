import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime
from schemas.user import User, UserCreate
import requests

back_url = "http://127.0.0.1:8000"

def login(user_id):
    get_user_url = back_url + '/get'
    user = requests.get(get_user_url, json=user_id)
    if not user:
        return False
    else:
        return user
dt_now = str(datetime.now().date())
dt_now = ''.join(c for c in dt_now if c not in '-')


#기본 페이지
st.title(':blue[Choose] The Stock You Want! :sunglasses:')
st.title('And :blue[Develop] Your Predictive Abilities!')

user_id = st.text_input("user_id")
if st.button("Login"):
    user = login(user_id)
    if user:#로그인 성공 시 및 유저 정보 get
        st.success(f"Hi! {user['name']}!!")
        #계정 수정
        if st.button("Revise"):
            user_name = st.text_input("user name")
            user_age = st.text_input("user age")
            user_priority = st.text_input("user_priority")
            user_info = User(
                user_name=user_name,
                age=user_age,
                priority=user_priority,
                score=user["score"],
                prediction=user["prediction"],
                delta = user["delta"],
            )
            revise_url = back_url + f"/revise/{user['id']}"
            response = requests.put(revise_url, json=user_info)

        #계정 삭제
        if st.button("Delete"):
            delete_url = back_url + f"/delete/{user['id']}"
            response = requests.delete(delete_url, json=user_info)

        #선호 주식 정보 제공
        data = stock.get_market_ohlcv("20011008", dt_now, user['priority'])
        data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
        st.write(f"{user['name']}'s Prefer Stock")
        st.write(data_df)
        st.line_chart(data_df['종가'])

        #현재 점수 제공
        st.metric(label=f"{user['name']}\'s Current Score", value = user['score'], delta = user['delta'], delta_color = 'inverse')
        
        #오늘의 주식 예측값 설정 및 저장
        st.write(f"{user['name']}'s today prediction!!")
        user['prediction'] = st.number_input("Enter Your Prediction")
        st.write(user['prediction'])
        
        #에어플로우를 통한 예측값 힌트로 제공 일단 지금은 안됨
        
         
    else:#로그인 실패시
        st.error("Invalid Username!")
        #기본 삼성 주식 정보 제공
        data = stock.get_market_ohlcv("20011008", dt_now, "005930")
        data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
        check = st.checkbox('I want to see the raw datas')
        if check:
            st.write(data_df)
        st.line_chart(data_df['종가'])

else:#로그인 시도 안 했을 때
    #새 계정 생성
    if st.button('Create New Account'):
        user_name = st.text_input("user name")
        user_age = st.text_input("user age")
        user_priority = st.text_input("user_priority")
        user_info = UserCreate(
            user_name=user_name,
            age=user_age,
            priority=user_priority,
            score=0,
            prediction=0,
        )
        if st.button('Create'):
            create_url = back_url + f"/create"
            response = requests.post(create_url, json=user_info)
    #기본 삼성 주식 정보 제공
    data = stock.get_market_ohlcv("20011008", dt_now, "005930")
    data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
    check = st.checkbox('I want to see the raw datas')
    if check:
        st.write(data_df)
    st.line_chart(data_df['종가'])

#랭킹 데이터 만들어서 추가
# all_data = pd.DataFrame(get_all_users())
# st.dataframe(all_data, use)
# st.table([(.name, person.age) for person in sorted_people])
