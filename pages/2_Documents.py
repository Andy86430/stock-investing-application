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
    page_options = ["Market_Timing", "Confirmed_Uptrend", "Stock_Screening", "Breakout_Setup", "Pullback_Setup", "Mistakes_to_Avoid"]
    selected_page = st.sidebar.selectbox("Documents", page_options)

    if selected_page == "Market_Timing":
        display_csv("Market_Timing")

    elif selected_page == "Confirmed_Uptrend":
        display_csv("Confirmed_Uptrend")

    elif selected_page == "Stock_Screening":
        display_csv("Stock_Screening")

    elif selected_page == "Breakout_Setup":
        display_csv("Breakout_Setup")

    elif selected_page == "Pullback_Setup":
        display_csv("Pullback_Setup")

    elif selected_page == "Mistakes_to_Avoid":
        display_csv("Mistakes_to_Avoid")

# Page config
st.set_page_config(page_title="Documents", page_icon="book")
st.sidebar.header("Documents")

documents()