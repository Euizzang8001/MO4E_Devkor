import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime
from schemas.user import User, UserCreate
import requests
import time

from pages.create import create_user

back_url = "http://127.0.0.1:8000/estock"
get_user_url = back_url + '/get'
dt_today = str(datetime.now().date())
dt_now = ''.join(c for c in dt_today if c not in '-')

if 'current' not in st.session_state:
    st.session_state['current'] = None

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
    st.write(f"{st.session_state.current['user_name']}'s Prefer Stock")
    st.write(data_df)
    st.line_chart(data_df['종가'])

    #현재 점수 제공
    st.metric(label=f"{st.session_state.current['user_name']}\'s Current Score", value = st.session_state.current['score'], delta = st.session_state.current['delta'], delta_color = 'inverse')
                
    #오늘의 주식 예측값 설정 및 저장
    st.write(f"{st.session_state.current['user_name']}'s today prediction!!")
    st.session_state.current['prediction'] = st.number_input("Enter Your Prediction")
    st.write(st.session_state.current['prediction'])    

#랭킹 데이터 -> 캐시데이터로 바꾸자
rank_url = back_url + '/rank'
rank_data = requests.get(rank_url).json()
first = rank_data['users'][0]['user_name']
st.title(f'{dt_today} TOP 10 RANK :sunglasses:')
st.write(f'Top 1 is {first}!')
rank_data_pd = pd.DataFrame(rank_data['users'], columns=['user_name', 'age', 'priority', 'score'])
st.table(rank_data_pd)