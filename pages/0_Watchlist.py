import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2 import service_account
from modules.functions import select_table
from modules.config import jscode_buy_range

def watchlist() -> None:

    # Connect to Google sheet
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(credentials)
    watchlist = client.open("Database").worksheet("Watchlist")
    watchlist_df = pd.DataFrame.from_dict(watchlist.get_all_records())

    # Interactive table
    df_sel_row = select_table(watchlist_df.loc[watchlist_df['Category'] == 'Watchlist'].sort_values("Buying Distance (%)"), jscode_buy_range)

    # Display the number of stocks
    message = "Number of stocks:"
    num_rows = len(watchlist_df.loc[watchlist_df['Category'] == 'Watchlist'])
    st.write(f"{message} {num_rows}")

    # Buttons to add and delete stocks from the table
    if not df_sel_row.empty:

        df_sel_row = df_sel_row.drop(columns='_selectedRowNodeInfo', axis=1)

        if st.button('Delete'):
            watchlist_updated = pd.concat([df_sel_row, watchlist_df]).drop_duplicates(keep=False)
            watchlist.clear()
            set_with_dataframe(worksheet=watchlist, dataframe=watchlist_updated, include_index=False, include_column_header=True, resize=True)
            st.experimental_rerun()

        if st.button('Add to portfolio'):
            watchlist_df.loc[((watchlist_df['Ticker'] == df_sel_row['Ticker'][0]) & (watchlist_df['Category'] == 'Watchlist') &
                            (watchlist_df['Trading Setup'] == df_sel_row['Trading Setup'][0])), 'Category'] = 'Portfolio'
            watchlist.clear()
            set_with_dataframe(worksheet=watchlist, dataframe=watchlist_updated, include_index=False, include_column_header=True, resize=True)
            st.experimental_rerun()

# Page config
st.set_page_config(page_title="Watchlist", page_icon="book")
st.markdown("# Watchlist")
st.sidebar.header("Watchlist")

watchlist()