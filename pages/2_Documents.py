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
    page_options = ["Mistakes to Avoid", "Investment Commandments", "Market Timing", "Confirmed Uptrend", 
                    "Stock Screener", "Trade Setup", "Climax Top", "Profit Taking", "Indicator Categories"]
    selected_page = st.sidebar.selectbox("Documents", page_options)

    if selected_page == "Mistakes to Avoid":
        display_csv("Mistakes to Avoid")

    elif selected_page == "Investment Commandments":
        display_csv("Investment Commandments")

    elif selected_page == "Market Timing":
        display_csv("Market Timing")

    elif selected_page == "Confirmed Uptrend":
        display_csv("Confirmed Uptrend")

    elif selected_page == "Stock Screener":
        display_csv("Stock Screener")

    elif selected_page == "Trade Setup":
        display_csv("Breakout Setup")
        display_csv("Pullback Setup")
        display_csv("Mean Reversion Setup")
        display_csv("Bullish Divergence Setup")
        display_csv("Coiled Spring Setup")

    elif selected_page == "Climax Top":
        display_csv("Climax Top")

    elif selected_page == "Profit Taking":
        display_csv("Profit Taking")

    elif selected_page == "Indicator Categories":
        display_csv("Indicator Categories")
        bullet_points = """
        - Volume is an independent variable hence volume indicators are preferred.
        - Avoid collinearity.
        - Focus on AD, II, MFI, VWMACD.
        """
        st.markdown(bullet_points)

# Page config
st.set_page_config(page_title="Documents", page_icon="book")
st.sidebar.header("Documents")

documents()