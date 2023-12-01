import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime
from schemas.user import User, UserCreate
import requests
import time

back_url = "http://127.0.0.1:8000/estock"

#new account

def create_user():
    st.title("Create New User")
    with st.form("Create"):
        user_name = st.text_input("Name")
        user_age = st.number_input("Age", value = 0, step=1, format="%d")
        user_priority = st.text_input("Prefer Stock Ticker You Want")
        new_info = {
            'user_name': user_name,
            'age': user_age,
            'priority': user_priority,
            'score': 0,
            'prediction': 0,
            'delta': 0,
        }
        create = st.form_submit_button("Create")
        if create:
            create_url = back_url + "/create"
            response = requests.post(create_url, json=new_info)
            if response.status_code == 200:
                st.write(f"Welcome to Stock Ed u! {user_name}!")
                st.session_state.current = None
                time.sleep(3)
                st.experimental_rerun()
            else:
                st.error(f"Error creating user: {response.text}")

if __name__ == "__main__":
    create_user()