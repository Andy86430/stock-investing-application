import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, JsCode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import json
import urllib
import streamlit as st
import yfinance as yf

# Interactive table
def select_table(df, jscode):
    """
    Create a table with selection capability
    :param df: dataframe to select from
    :return: selected rows
    """

    gd = GridOptionsBuilder.from_dataframe(df)
    cellsytle_jscode = JsCode(jscode)
    gd.configure_columns(
        (
            "Buying Distance (%)",
        ),
        cellStyle=cellsytle_jscode,
    )
    gd.configure_pagination(enabled=True)
    gd.configure_columns(("Ticker", "Buying Distance (%)"), pinned=True)
    gd.configure_default_column(editable=True, groupable=True)
    gd.configure_selection(selection_mode="multiple", use_checkbox=True)
    gridoptions = gd.build()
    grid_table = AgGrid(
        df,
        gridOptions=gridoptions,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        theme="material",
        allow_unsafe_jscode=True,
    )

    return pd.DataFrame(grid_table["selected_rows"])

# Find the PS ratio of a stock
def get_PSratio(Symbol):

    api = "e2ddb9db079212837b432d1641354915"
    url = f"https://financialmodelingprep.com/api/v3/ratios-ttm/{Symbol}?apikey={api}"
    response = urllib.request.urlopen(url)
    data = response.read().decode("utf-8")
    data = json.loads(data)

    try:
        return data[0]['priceToSalesRatioTTM']
    except Exception as e:
        return 0

# This funtion scraps each Symbol page and extract the Zacks Rank
def Zacks_Rank(Symbol):

    url = 'https://quote-feed.zacks.com/index?t=' + Symbol
    downloaded_data = urllib.request.urlopen(url)
    data = downloaded_data.read()
    data_str = data.decode()
    Z_Rank = ["Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]

    for Rank in Z_Rank:
        if data_str.find(Rank) != -1:
            return Rank
        
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

# Get the live stock price
def stock_price(Symbol):
    stock_info = yf.Ticker(Symbol).info
    price = stock_info['currentPrice']
    return price

# starts_with_letter_from_list
def starts_with_letter_from_list(string, letter_list):
    for letter in letter_list:
        if string.startswith(letter):
            return True
    return False

# Define conditional formatting function
def highlight_cells(val):
    if val.name == "Zack Rank":
        return ['background-color: green' if x in ["Strong Buy", "Buy"] else 'background-color: red' for x in val]
    
    elif val.name == "IBD Market Outlook":
        return ['background-color: green' if x == "Confirmed Uptrend" else 'background-color: red' for x in val]
    
    elif val.name == "OBV" or val.name == "MACD line (not signal line)":
        return ['background-color: green' if x == "At/Near New High" else 'background-color: red' for x in val]
    
    elif val.name == '%b':
        return ['background-color: green' if x >= 0.8 else 'background-color: orange' for x in val]
    
    elif val.name == 'MFI (10)':
        return ['background-color: green' if x >= 80 else 'background-color: orange' for x in val]
    
    elif val.name == 'Bollinger Squeeze' or val.name == 'Leaderboard':
        return ['background-color: green' if x == "Yes" else 'background-color: orange' for x in val]
    
    elif val.name == 'Type of Base':
        return ['background-color: green' if x == "Cup with Handle" else 'background-color: orange' for x in val]
    
    elif val.name == 'Stage':
        return ['background-color: green' if str(x).startswith(('1', '2')) else 'background-color: orange' if str(x).startswith(('3')) else 'background-color: orange' for x in val]
    
    elif val.name == 'Base Depth':
        return ['background-color: red' if float(x.strip('%')) > 30 else 'background-color: green' for x in val]
    
    elif val.name == 'Breakout Vol% (Daily)' or val.name == 'Breakout Vol% (Weekly)':
        return ['background-color: green' if float(x.strip('%')) >= 40 else 'background-color: red' if float(x.strip('%')) < 0 else 'background-color: orange' for x in val]
    
    elif val.name == 'Handle Depth':
        return ['background-color: orange' if x=="N/A" else 'background-color: red' if float(x.strip('%')) > 15 else 'background-color: green' for x in val]
    
    elif val.name == '50-Day > 150-Day > 200-Day' or val.name == 'RS Line Within 5% of New High':
        return ['background-color: green' if x == 1 else 'background-color: red' for x in val]
    
    elif val.name == 'EPS Rating' or val.name == 'Comp Rating':
        return ['background-color: green' if x >= 80 else 'background-color: red' for x in val]

    elif val.name == 'RS Rating':
        return ['background-color: green' if x >= 90 else 'background-color: red' if x < 80 else 'background-color: orange' for x in val]

    elif val.name == 'SMR Rating' or val.name == 'A/D Rating' or val.name == 'Timeliness Rating':
        return ['background-color: green' if starts_with_letter_from_list(x,["A","B","C"]) else 'background-color: red' for x in val]

    elif val.name == 'Ind Group RS' or val.name == 'Sponsor Rating':
        return ['background-color: green' if starts_with_letter_from_list(x,["A","B","C","D"]) else 'background-color: red' for x in val]

    elif val.name == 'Price to Sales':
        return ['background-color: green' if x <= 3 else 'background-color: orange' for x in val]

    elif val.name == '50-Day Avg Vol (1000s)':
        return ['background-color: green' if x >= 400 else 'background-color: red' for x in val]
    
    elif val.name == 'Ind Group Rank':
        return ['background-color: green' if x <= 40 else 'background-color: orange' for x in val]

    if val.name == "No. of Funds - Last 4 Qtrs":
        return ['background-color: red' if x in ["Decreasing", "Decreased"] else 'background-color: green' for x in val]

    if val.name == "Sales % Chg Lst Qtr":

        # Extract values from the specified columns
        val1 = row["Sales % Chg 2 Q Ago"]
        val2 = row["Sales % Chg 1 Q Ago"]
        val3 = row["Sales % Chg Lst Qtr"]

        # Compare the values
        if val3 > val2 and val2 > val1:
            return ['background-color: green'] * len(row)
        else:
            return [''] * len(row) 

    else:
        return [''] * len(val)