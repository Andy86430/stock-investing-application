import streamlit as st
import pandas as pd
from modules.functions import get_PSratio
from modules.functions import convert_df
from modules.functions import Zacks_Rank
# from modules.functions import stock_price
# from gspread_dataframe import set_with_dataframe
# import gspread
# from google.oauth2 import service_account

def run():
    
    # Page config
    st.set_page_config(
        page_title="Market Wizard",
        page_icon="chart_with_upwards_trend",
    )

    st.write(Zacks_Rank("AAPL"))
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
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"])
        client = gspread.authorize(credentials)
        stocklist = client.open("Database").worksheet("Stock_List")
        stocklist_df = pd.DataFrame.from_dict(stocklist.get_all_records())
        stocklist_df['Price'] = stocklist_df['Ticker'].apply(lambda x: stock_price(x)).round(2)
        stocklist_df['Buying Distance (%)'] = (100 * (stocklist_df['Price'] / stocklist_df['Buy Point'] - 1)).round(1)
        stocklist_df['Zacks Rank'] = stocklist_df['Ticker'].apply(lambda x: Zacks_Rank(x))
        stocklist.clear()
        set_with_dataframe(worksheet=stocklist, dataframe=stocklist_df, include_index=False, include_column_header=True, resize=True)

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