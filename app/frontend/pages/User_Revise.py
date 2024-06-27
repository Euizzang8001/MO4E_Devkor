import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime
from schemas.user import User, UserCreate, UserRevise
import requests
import time

back_url = "http://backend/estock"

def revise_user(user):
    st.title("Revise Your Information")
    with st.form("revise"):
        revise_url = back_url + f"/revise/{user['user_id']}"
        user_name = st.text_input("user name")
        user_age = st.number_input("user age", value = 0, step=1, format="%d")
        revise_button = st.form_submit_button("Revise")
        user_info = {
            'user_name': user_name,
            'age': user_age,
            'score': user['score'],
            'prediction': user['prediction'],
            'delta': user['delta'],
        }
        if revise_button:
            response = requests.put(revise_url, params={'user_id': user['user_id']}, json = user_info)
            if response.status_code == 200:
                st.write(f"Revise Success! Please Log In Again, {user_name}!")
                st.session_state.current = None
                time.sleep(3)
                st.experimental_rerun()
            else:
                st.error(f"Error creating user: {response.text}")

if __name__ == "__main__" and st.session_state.current != None:
    revise_user(st.session_state.current)
else:
    st.error("Please Login and Revisit Again")