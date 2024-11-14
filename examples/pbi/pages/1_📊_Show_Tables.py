import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Show Tables", page_icon="🌍")
st.markdown("# Show Tables")
st.sidebar.header("# Show Tables")

files={
    'items': './items.xlsx',
    'sales': './sales.xlsx'
}
items=pd.read_excel(files['items'], index_col=0)
sales=pd.read_excel(files['sales'], index_col=0)

st.write("商品マスタ")
items
st.write("売上データ")
sales
st.write("リレーションされた売上データ")
merged_sales = pd.merge(sales, items, how='inner', on='商品ID')
#merged_sales
merged_sales[['商品ID', '商品名', '販売数量', '値段']]
