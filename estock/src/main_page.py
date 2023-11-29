import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime
from schemas.user import User, UserCreate
import requests

def revise(user):
    with st.form("revise"):
        revise_url = back_url + f"/revise/{user['user_id']}"
        user_name = st.text_input("user name")
        user_age = st.number_input("user age", value = 0, step=1, format="%d")
        user_priority = st.text_input("user_priority")
        user_info = User(
                    user_name=user_name,
                    age=user_age,
                    priority=user_priority,
                    score=user["score"],
                    prediction=user["prediction"],
                    delta = user["delta"],
                    )
        if st.button("Real Revise"):
            response = requests.put(revise_url, params={'user_id': user_id, 'user_revise_dto': user_info})


back_url = "http://127.0.0.1:8000/estock"
get_user_url = back_url + '/get'
dt_today = str(datetime.now().date())
dt_now = ''.join(c for c in dt_today if c not in '-')


#기본 페이지
st.title(':blue[Choose] The Stock You Want! :sunglasses:')
st.title('And :blue[Develop] Your Predictive Abilities!')

user_id = st.text_input("user_id")
if st.button("Login"):
    user = login(user_id)
    if user:#로그인 성공 시 및 유저 정보 get
        user = user.json()
        st.success(f"Hi! {user['user_name']}!!")

        #계정 정보 수정
        if st.button("Revise"):
            with st.form("revise"):
                revise_url = back_url + f"/revise/{user['user_id']}"
                user_name = st.text_input("user name")
                user_age = st.number_input("user age", value = 0, step=1, format="%d")
                user_priority = st.text_input("user_priority")
                user_info = User(
                            user_name=user_name,
                            age=user_age,
                            priority=user_priority,
                            score=user["score"],
                            prediction=user["prediction"],
                            delta = user["delta"],
                            )
            if st.button("Real Revise"):
                response = requests.put(revise_url, params={'user_id': user_id, 'user_revise_dto': user_info})                

        #계정 삭제
        if st.button("Delete"):
            delete_url = back_url + f"/delete/{user['user_id']}"
            response = requests.delete(delete_url, params={'user_id': user_id})

        #선호 주식 정보 제공
        data = stock.get_market_ohlcv("20011008", dt_now, user['priority'])
        data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
        st.write(f"{user['user_name']}'s Prefer Stock")
        st.write(data_df)
        st.line_chart(data_df['종가'])

        #현재 점수 제공
        st.metric(label=f"{user['user_name']}\'s Current Score", value = user['score'], delta = user['delta'], delta_color = 'inverse')
        
        #오늘의 주식 예측값 설정 및 저장
        st.write(f"{user['user_name']}'s today prediction!!")
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
        user_age = st.number_input("user age", value = 0, step=1, format="%d")
        user_priority = st.text_input("user_priority")
        user_info = UserCreate(
            user_name=user_name,
            age=user_age,
            priority=user_priority,
            score=0,
            prediction=0,
            delta=0,
        )
        if st.button('Create'):
            create_url = back_url + f"/create"
            response = requests.post(create_url, params = {'user_create_dto': user_info})
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
rank_url = back_url + '/rank'
rank_data = requests.get(rank_url).json()
first = rank_data['users'][0]['user_name']
st.title(f'{dt_today} TOP 10 RANK :sunglasses:')
st.write(f'Top 1 is {first}!')
rank_data_pd = pd.DataFrame(rank_data['users'], columns=['user_name', 'age', 'priority', 'score'])
st.table(rank_data_pd)