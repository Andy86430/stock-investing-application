import streamlit as st
import pandas as pd
from gspread_dataframe import set_with_dataframe
from modules.functions import select_table
from modules.config import jscode_buy_range

def watchlist() -> None:

    # Connect to Google sheet
    from streamlit_app import watchlist, portfolio
    watchlist_df = pd.DataFrame.from_dict(watchlist.get_all_records())
    portfolio_df = pd.DataFrame.from_dict(portfolio.get_all_records())

    # Interactive table
    df_sel_row = select_table(watchlist_df.sort_values("Buying Distance (%)"), jscode_buy_range)

    # Display the number of stocks
    message = "Number of stocks:"
    num_rows = len(watchlist_df)
    st.write(f"{message} {num_rows}")

    # Buttons to add and delete stocks from the table
    if not df_sel_row.empty:

        df_sel_row = df_sel_row.drop(columns='_selectedRowNodeInfo', axis=1)

        if st.button('Delete'):
            watchlist_df_updated = pd.concat([df_sel_row, watchlist_df]).drop_duplicates(keep=False)
            watchlist.clear()
            set_with_dataframe(worksheet=watchlist, dataframe=watchlist_df_updated, include_index=False, include_column_header=True)
            st.experimental_rerun()

        if st.button('Add to portfolio'):
            portfolio_df_updated = pd.concat([df_sel_row, portfolio_df])
            portfolio.clear()
            set_with_dataframe(worksheet=portfolio, dataframe=portfolio_df_updated, include_index=False, include_column_header=True, resize=True)
            st.experimental_rerun()

# Page config
st.set_page_config(page_title="Watchlist", page_icon="book")
st.markdown("# Watchlist")
st.sidebar.header("Watchlist")

watchlist()