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
    page_options = ["Mistakes to Avoid", "Investment Commandments", "Market Timing", "Stock Confirmed Uptrend", "Market Top", 
                    "Climax Top", "Profit Taking", "Indicator Categories", 
                    "Find The Best IPO Stocks",
                    "Breakout Strategy", "Pullback Strategy"]
    selected_page = st.sidebar.selectbox("Documents", page_options)

    if selected_page == "Mistakes to Avoid":
        display_csv("Mistakes to Avoid")

    elif selected_page == "Investment Commandments":
        display_csv("Investment Commandments")

    elif selected_page == "Market Timing":
        display_csv("Market Timing")

    elif selected_page == "CStock Confirmed Uptrend":
        display_csv("Stock Confirmed Uptrend")

    elif selected_page == "Breakout Strategy":
        display_csv("Breakout Strategy")

    elif selected_page == "Pullback Strategy":
        display_csv("Pullback Setup")
        display_csv("Pullback Screener")

    elif selected_page == "Climax Top":
        display_csv("Climax Top")

    elif selected_page == "Find The Best IPO Stocks":
        display_csv("Find The Best IPO Stocks")

    elif selected_page == "Profit Taking":
        display_csv("Profit Taking")

    elif selected_page == "Market Top":
        display_csv("Market Top")

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