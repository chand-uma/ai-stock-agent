import streamlit as st
import matplotlib.pyplot as plt

st.title("AI Trading Dashboard")
st.line_chart(data['Adj Close'])

# Add performance metrics
st.write("Current Balance:", balance)
st.write("Open Positions:", open_positions)
