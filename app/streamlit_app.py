import httpx
import streamlit as st

API_URL = "http://127.0.0.1:8000/hello"

st.title("Hello World App")

if st.button("Say Hello"):
    response = httpx.get(API_URL)
    data = response.json()
    st.success(data["message"])
