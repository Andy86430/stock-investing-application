import streamlit as st
import pandas as pd
from gspread_dataframe import set_with_dataframe
from modules.functions import select_table
from modules.config import jscode_buy_range
from modules.functions import stock_price
from modules.functions import Zacks_Rank
from modules.functions import highlight_cells
from modules.functions import highlight_cells_ascending
from streamlit_app import df_breakout, df_pullback, df_coil
from modules.functions import from_google_sheet
from streamlit_app import client

df_breakout = from_google_sheet(client, "Breakout Candidate")
df_pullback = from_google_sheet(client, "Pullback Candidate")
df_coil = from_google_sheet(client, "Coiled Spring Candidate")

def display_csv(df):

    # Add a multiselect widget to select rows based on the index
    selected_indices = st.multiselect('Select Stocks:', df.index)

    # Subset the dataframe with the selected indices
    selected_rows = df.loc[selected_indices]

    # Apply the conditional formatting to the specified columns in DataFrame
    sales_col = ['Sales % Chg 2 Q Ago', 'Sales % Chg 1 Q Ago', 'Sales % Chg Lst Qtr']
    EPS_col = ['EPS % Chg 2 Q Ago (-/+)','EPS % Chg 1 Q Ago (-/+)','EPS % Chg Last Qtr (-/+)']
    styled_df = selected_rows.style.apply(highlight_cells, axis=0).apply(highlight_cells_ascending, subset=sales_col, axis=1).apply(highlight_cells_ascending, subset=EPS_col, axis=1)

    st.write(styled_df, use_container_width=True)

def watchlist() -> None:

    # Connect to Google sheet
    from streamlit_app import watchlist, portfolio
    watchlist_df = pd.DataFrame.from_dict(watchlist.get_all_records())
    portfolio_df = pd.DataFrame.from_dict(portfolio.get_all_records())

    # Add a stock
    cols = st.columns(3)
    ticker = cols[0].text_input("Ticker:")
    setup = cols[1].selectbox("Trading Setup:", ["Breakout", "Pullback"], index=0)
    buy_point = cols[2].text_input("Buy Point:")
    if st.button(label="Submit"):
        new_row = pd.DataFrame(
            {'Ticker': [ticker], 'Trading Setup': [setup], 'Buy Point': [buy_point], 'Price': [round(stock_price(ticker), 2)],
             'Zacks Rank': [Zacks_Rank(ticker)]})
        new_row['Buying Distance (%)'] = (100 * (new_row['Price'] / new_row['Buy Point'].astype(float) - 1)).round(1)
        watchlist_df_updated = watchlist_df.append(new_row, ignore_index=True)
        watchlist.clear()
        set_with_dataframe(worksheet=watchlist, dataframe=watchlist_df_updated, include_index=False, include_column_header=True)
        st.experimental_rerun()

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

    st.title("Breakout Candidate")
    display_csv(df_breakout)

    st.title("Pullback Candidate")
    display_csv(df_pullback)

    st.title("Coiled Spring Candidate")
    display_csv(df_coil)

# Page config
st.set_page_config(page_title="Watchlist", page_icon="book")
st.markdown("# Watchlist")
st.sidebar.header("Watchlist")

watchlist()