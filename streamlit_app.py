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
global watchlist
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credentials)
watchlist = client.open("Database").worksheet("Watchlist")

def run():
    
    # Page config
    st.set_page_config(
        page_title="Market Wizard",
        page_icon="chart_with_upwards_trend",
    )

    # Produce a bullish watchlist
    st.markdown("""### Actions:""")
    upload = st.file_uploader('Upload Stock List (xlsx)', type="csv")
    if upload is not None:
        if st.button('Produce Bullish List'):    
            bullishlist = pd.read_csv(upload).dropna()
            bullishlist['Zack Rank'] = bullishlist['Symbol'].apply(lambda x: Zacks_Rank(x))
            bullishlist = bullishlist.loc[(bullishlist['Zack Rank'].isin(['Buy', 'Strong Buy']))]
            bullishlist['PS'] = bullishlist['Symbol'].apply(lambda x: get_PSratio(x))
            bullishlist = bullishlist.sort_values(by=['PS'])
            csv = convert_df(bullishlist['Symbol'])
            st.download_button("Download",csv,upload.name.replace(".csv"," Filtered")+".csv","text/csv",key='download-csv')

    # Refresh stock prices
    if st.button('Refresh'):

        global watchlist

        # Refresh watchlist
        watchlist_df = pd.DataFrame.from_dict(watchlist.get_all_records())
        watchlist_df['Zacks Rank'] = watchlist_df['Ticker'].apply(lambda x: Zacks_Rank(x))
        watchlist.clear()
        set_with_dataframe(worksheet=watchlist, dataframe=watchlist_df, include_index=False, include_column_header=True)
        st.success("Successful!")

    # Useful links
    st.markdown(
        """
        ### Useful Websites:
        - [Zacks](https://www.zacks.com)
        - [TradingView](https://www.tradingview.com/chart/3JwfLY94)
        - [Tipranks](https://www.tipranks.com/dashboard)
        - [IBD](https://www.investors.com/)
        - [MarketSmith](https://marketsmith.investors.com/)
    """
    )


if __name__ == "__main__":
    run()