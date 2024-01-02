import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2 import service_account
from modules.functions import select_table
from modules.config import jscode_buy_range

def portfolio() -> None:

    # Connect to Google sheet
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(credentials)
    portfolio = client.open("Database").worksheet("Portfolio")
    portfolio_df = pd.DataFrame.from_dict(portfolio.get_all_records())

    # Interactive table
    df_sel_row = select_table(portfolio_df.sort_values("Buying Distance (%)"), jscode_buy_range)

    # Display the number of stocks
    message = "Number of stocks:"
    num_rows = len(portfolio_df)
    st.write(f"{message} {num_rows}")

    # Buttons to add and delete stocks from the table
    if not df_sel_row.empty:

        df_sel_row = df_sel_row.drop(columns='_selectedRowNodeInfo', axis=1)

        if st.button('Delete'):
            portfolio_df_updated = pd.concat([df_sel_row, portfolio_df]).drop_duplicates(keep=False)
            portfolio.clear()
            set_with_dataframe(worksheet=portfolio, dataframe=portfolio_df_updated, include_index=False, include_column_header=True)
            st.experimental_rerun()

        # if st.button('Add to portfolio'):
        #     portfolio_df.loc[((portfolio_df['Ticker'] == df_sel_row['Ticker'][0]) & (portfolio_df['Category'] == 'portfolio') &
        #                     (portfolio_df['Trading Setup'] == df_sel_row['Trading Setup'][0])), 'Category'] = 'Portfolio'
        #     portfolio.clear()
        #     set_with_dataframe(worksheet=portfolio, dataframe=portfolio_updated, include_index=False, include_column_header=True, resize=True)
        #     st.experimental_rerun()

# Page config
st.set_page_config(page_title="Portfolio", page_icon="book")
st.markdown("# Portfolio")
st.sidebar.header("Portfolio")

portfolio()
