import streamlit as st
import pandas as pd
import numpy as np
from pykrx import stock
from datetime import datetime
from schemas.user import User, UserCreate, UserRevise
import requests
import time

back_url = "http://127.0.0.1:8000/estock"

def delete_user(user):
    st.title("Delete your information")
    delete_url = back_url + f"/delete/{user['user_id']}"
    delete_button = st.button("Delete")
    if delete_button:
        response = requests.delete(delete_url, params={'user_id': user['user_id']})
        if response.status_code == 200:
            st.write(f"See You Again! {st.session_state.current['user_name']}!")
            st.session_state.current = None
            time.sleep(3)
            st.experimental_rerun()
        else:
            st.error(f"Error creating user: {response.text}")

if __name__ == "__main__" and st.session_state.current != None:
    delete_user(st.session_state.current)
else:
    st.error("Please Login and Revisit Again")
