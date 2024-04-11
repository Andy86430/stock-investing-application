import streamlit as st
import pandas as pd
from modules.functions import highlight_cells
from modules.functions import highlight_cells_ascending
from modules.functions import from_google_sheet
from streamlit_app import client

# Page config
st.set_page_config(page_title="Deep Analysis", page_icon="analysis")
st.markdown("# Deep Analysis")
st.sidebar.header("Deep Analysis")

df_breakout = from_google_sheet(client, "Breakout Candidate")
df_breakout_offline = df_breakout.copy()
df_pullback = from_google_sheet(client, "Pullback Candidate")
df_pullback_offline = df_pullback.copy()
df_coil = from_google_sheet(client, "Coiled Spring Candidate")
df_coil_offline = df_coil.copy()

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

st.title("Breakout Candidate")
display_csv(df_breakout_offline)

st.title("Pullback Candidate")
display_csv(df_pullback_offline)

st.title("Coiled Spring Candidate")
display_csv(df_coil_offline)