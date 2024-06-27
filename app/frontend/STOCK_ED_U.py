import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime
import requests
import time


back_url = "http://backend/estock"
get_user_url = back_url + '/get'
dt_today = str(datetime.now().date())
dt_now = ''.join(c for c in dt_today if c not in '-')

if 'current' not in st.session_state:
    st.session_state['current'] = None

def revise_prediction(user, today_prediction):
    revise_pred_url = back_url + f"/revise/{user['user_id']}"
    user_info = {
        'user_name': user['user_name'],
        'age': user['age'],
        'priority': user['priority'],
        'score': user['score'],
        'prediction': today_prediction,
        'delta': user['delta'],
    }
    response = requests.put(revise_pred_url, params={'user_id': user['user_id']}, json = user_info)

    if response.status_code == 200:
        st.success(f"Prediction Score Success!")
        st.session_state.current['prediction'] = today_prediction
        time.sleep(2)
        st.experimental_rerun()
    else:
        st.error(f"Error creating user: {response.text}")

#기본 페이지
st.title(':blue[Choose] The Stock You Want! :sunglasses:')
st.title('And :blue[Develop] Predictive Abilities!')

#session에 현재 로그인 정보가 없으면
if not st.session_state['current']:
    #로그인
    user_id = st.text_input("ID")
    login_button = st.button("Login")
    if login_button:
        user = requests.get(get_user_url, params={'user_id': user_id})
        if user:#로그인 성공 시 및 유저 정보 get
            user_info = user.json()
            st.session_state['current'] = user_info
            st.success(f"Hi! {user_info['user_name']}!!")
            time.sleep(3)
            st.experimental_rerun()
                
        else:#로그인 실패시
            st.error("Invalid Username!")
    #새계정 생성 -> create.py

    #기본 삼성 주식 정보 제공
    st.header('Samsung Stock Data')
    data = stock.get_market_ohlcv("20011008", dt_now, "005930")
    data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
    check = st.checkbox('I want to see the raw datas')
    if check:
        st.write(data_df)
    st.line_chart(data_df['종가'])

else:#현재 로그인 정보가 있으면
    #로그아웃
    if st.button("Logout"):
        st.success(f"See You Next Time, {st.session_state['current']['user_name']}!")
        st.session_state['current'] = False
        time.sleep(3)
        st.experimental_rerun()

    #계정 정보 수정 -> revise.py
    #계정 정보 삭제 -> delete.py

    #선호 주식 정보 제공
    data = stock.get_market_ohlcv("20011008", dt_now, st.session_state.current['priority'])
    data_df = pd.DataFrame(data, columns=["시가", "고가", "저가", "종가", "거래량"])
    st.header(f"{st.session_state.current['user_name']}'s Prefer Stock")
    st.write(data_df)
    st.line_chart(data_df['종가'])

    #현재 점수 제공
    st.metric(label=f"{st.session_state.current['user_name']}\'s Current Score", value = st.session_state.current['score'], delta = st.session_state.current['delta'], delta_color = 'inverse')
                
    #오늘의 주식 예측값 설정 및 저장
    st.header(f"{st.session_state.current['user_name']}'s Today Prediction: {st.session_state.current['prediction']}won")
    today_prediction = st.number_input("Enter Your Prediction", value = st.session_state.current['prediction'], step=1, format="%d")
    #주식 예측값 제시 -> airflow로 해야할 것 같다..
    prediction_url = back_url + '/get-stock'
    stock_prediction = requests.get(prediction_url, params={'date': dt_today})
    st.write(f"Hint(LSTM prediction: {stock_prediction['samsung_lstm']}won")
    revise_prediction_button = st.button("Revise My Prediction")
    if revise_prediction_button:
        revise_prediction(st.session_state.current, today_prediction)

#랭킹 데이터 -> 캐시데이터로 바꾸자
rank_url = back_url + '/rank'
rank_data = requests.get(rank_url).json()
first = rank_data['users'][0]['user_name']
st.title(f'{dt_today} TOP 10 RANK :sunglasses:')
st.header(f'Top 1 is {first}!')
rank_data_pd = pd.DataFrame(rank_data['users'], columns=['user_name', 'age', 'priority', 'score'])
st.table(rank_data_pd)