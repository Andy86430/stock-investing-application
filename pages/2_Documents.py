import streamlit as st
import pandas as pd

def display_csv(name):

    # Display a Google sheet
    from streamlit_app import client
    wks = client.open("Database").worksheet(name)
    df = pd.DataFrame.from_dict(wks.get_all_records())
    df = df.set_index(df.columns[0])
    st.title(name)
    st.table(df)

def documents() -> None:

    # Sidebar navigation
    page_options = ["Mistakes to Avoid", "Market Timing", "Confirmed Uptrend", "Stock Screener", "Breakout Setup", "Pullback Setup"]
    selected_page = st.sidebar.selectbox("Documents", page_options)

    if selected_page == page_options[0]:
        display_csv(page_options[0])

    elif selected_page == page_options[1]:
        display_csv(page_options[1])

    elif selected_page == page_options[2]:
        display_csv(page_options[2])

    elif selected_page == page_options[3]:
        display_csv(page_options[3])

    elif selected_page == page_options[4]:
        display_csv(page_options[4])

    elif selected_page == page_options[5]:
        display_csv(page_options[5])

# Page config
st.set_page_config(page_title="Documents", page_icon="book")
st.sidebar.header("Documents")

documents()