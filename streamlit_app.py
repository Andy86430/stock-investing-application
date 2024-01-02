import streamlit as st
import pandas as pd
from modules.functions import get_PSratio
from modules.functions import convert_df
from modules.functions import Zacks_Rank
from modules.functions import stock_price
from gspread_dataframe import set_with_dataframe
import gspread
from google.oauth2 import service_account

# Connect to Google sheet
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credentials)
watchlist = client.open("Database").worksheet("Watchlist")
portfolio = client.open("Database").worksheet("Portfolio")

def run():
    
    # Page config
    st.set_page_config(
        page_title="Market Wizard",
        page_icon="chart_with_upwards_trend",
    )

    # Produce a bullish watchlist
    st.markdown("""### Actions:""")
    upload = st.file_uploader('Upload "IBD Data Tables.xlsx"', type="xlsx")
    if upload is not None:
        if st.button('Produce Bullish List'):    
            watchlist = pd.read_excel(upload).dropna()
            watchlist = watchlist.rename(columns=watchlist.iloc[0]).drop(watchlist.index[0])
            watchlist['Zack Rank'] = watchlist['Symbol'].apply(lambda x: Zacks_Rank(x))
            watchlist = watchlist.loc[(watchlist['Zack Rank'].isin(['Buy', 'Strong Buy']))]
            watchlist['PS'] = watchlist['Symbol'].apply(lambda x: get_PSratio(x))
            watchlist = watchlist.sort_values(by=['PS'])
            csv = convert_df(watchlist['Symbol'])
            st.download_button("Download",csv,"Bullish List.csv","text/csv",key='download-csv')

    # Refresh stock prices
    if st.button('Refresh'):

        # Refresh watchlist
        watchlist_df = pd.DataFrame.from_dict(watchlist.get_all_records())
        watchlist_df['Price'] = watchlist_df['Ticker'].apply(lambda x: stock_price(x)).round(2)
        watchlist_df['Buying Distance (%)'] = (100 * (watchlist_df['Price'] / watchlist_df['Buy Point'] - 1)).round(1)
        watchlist_df['Zacks Rank'] = watchlist_df['Ticker'].apply(lambda x: Zacks_Rank(x))
        watchlist.clear()
        set_with_dataframe(worksheet=watchlist, dataframe=watchlist_df, include_index=False, include_column_header=True)

        # Refresh portfolio
        portfolio_df = pd.DataFrame.from_dict(portfolio.get_all_records())
        portfolio_df['Price'] = portfolio_df['Ticker'].apply(lambda x: stock_price(x)).round(2)
        portfolio_df['Buying Distance (%)'] = (100 * (portfolio_df['Price'] / portfolio_df['Buy Point'] - 1)).round(1)
        portfolio_df['Zacks Rank'] = portfolio_df['Ticker'].apply(lambda x: Zacks_Rank(x))
        portfolio.clear()
        set_with_dataframe(worksheet=portfolio, dataframe=portfolio_df, include_index=False, include_column_header=True)

    # Useful links
    st.markdown(
        """
        ### Useful Websites:
        - [Zacks](https://www.zacks.com)
        - [TradingView](https://www.tradingview.com/chart/3JwfLY94)
        - [Tipranks](https://www.tipranks.com/dashboard)
        - [IBD](https://www.investors.com/)
    """
    )


if __name__ == "__main__":
    run()