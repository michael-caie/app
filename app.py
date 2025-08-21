import streamlit as st

st.title("My First Streamlit App")
st.write("Hello, world!")

number = st.slider("Pick a number", 0, 100)
st.write("You picked:", number)
