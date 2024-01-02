import streamlit as st
import pandas as pd

def display_csv(name):

    # Display a Google sheet
    from streamlit_app import client
    wks = client.open("Database").worksheet(name)
    df = pd.DataFrame.from_dict(wks.get_all_records(), index_col=0)
    st.title(name)
    st.table(df)

def documents() -> None:

    # Sidebar navigation
    page_options = ["Confirmed_Uptrend", "Stock Screen", "Breakout Setup", "Pullback Setup", "Bullish Candle Formations"]
    selected_page = st.sidebar.selectbox("Documents", page_options)

    if selected_page == "Confirmed_Uptrend":
        display_csv("Confirmed_Uptrend")

    elif selected_page == "Stock Screen":
        display_csv("Stock Screen")

    elif selected_page == "Breakout Setup":
        display_csv("Breakout Setup")

    elif selected_page == "Pullback Setup":
        display_csv("Pullback Setup")

    elif selected_page == "Bullish Candle Formations":
        st.image('hammer.jpeg', caption='Hammer')
        st.image('Piercing.png', caption='Piercing')
        st.image('Engulfing.png', caption='Piercing')
        st.image('Morning Star.jpeg', caption='Piercing')


# Page config
st.set_page_config(page_title="Documents", page_icon="book")
st.sidebar.header("Documents")

documents()