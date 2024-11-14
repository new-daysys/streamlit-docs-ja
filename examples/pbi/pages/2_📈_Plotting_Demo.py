import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.markdown("# Plotting Demo")
st.sidebar.header("# Plotting Demo")

files={
    'items': './items.xlsx',
    'sales': './sales.xlsx'
}
items=pd.read_excel(files['items'])
sales=pd.read_excel(files['sales'])
merged_sales = pd.merge(sales, items, how='inner', on='商品ID')
#merged_sales[['商品ID', '商品名', '販売数量', '値段']]
merged_sales[['商品名', '値段']]
selected = st.sidebar.multiselect('Items', items['商品名'], items['商品名'])
item_select = alt.selection_single(fields=["selected"], empty="all")
region_pie = (
    (
        alt.Chart(merged_sales)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(
                '値段',
                type="quantitative",
                aggregate="sum",
                title="Sum of item",
            ),
            color=alt.Color(
                field="商品名",
                type="nominal",
                scale=alt.Scale(domain=items['商品名'], scheme='category20'),
                title="Item",
            ),
            opacity=alt.condition(item_select, alt.value(1), alt.value(0.25)),
        )
        .add_selection(item_select)
        .properties(title="Sales by Item")
    )
)
region_pie

#_='''
regions = ["LATAM", "EMEA", "NA", "APAC"]
colors = [
    "#aa423a",
    "#f6b404",
    "#327a88",
    "#303e55",
    "#c7ab84",
    "#b1dbaa",
    "#feeea5",
    "#3e9a14",
    "#6e4e92",
    "#c98149",
    "#d1b844",
    "#8db6d8",
]
months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

@st.cache_data
def get_data():
    dates = pd.date_range(start="1/1/2022", end="12/31/2022")
    data = pd.DataFrame()
    sellers = {
        "LATAM": ["S01", "S02", "S03"],
        "EMEA": ["S10", "S11", "S12", "S13"],
        "NA": ["S21", "S22", "S23", "S24", "S25", "S26"],
        "APAC": ["S31", "S32", "S33", "S34", "S35", "S36"],
    }
    rows = 25000
    data["transaction_date"] = np.random.choice([str(i) for i in dates], size=rows)
    data["region"] = np.random.choice(regions, size=rows, p=[0.1, 0.3, 0.4, 0.2])
    data["transaction_amount"] = np.random.uniform(100, 250000, size=rows).round(2)
    data["seller"] = data.apply(
        lambda x: np.random.choice(sellers.get(x["region"])), axis=1
    )
    return data.sort_values(by="transaction_date").reset_index(drop=True)


sales_data = get_data()

region_select = alt.selection_single(fields=["region"], empty="all")
region_select
region_pie = (
    (
        alt.Chart(sales_data)
        .mark_arc(innerRadius=50)
        .encode(
            theta=alt.Theta(
                "transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Sum of Transactions",
            ),
            color=alt.Color(
                field="region",
                type="nominal",
#                scale=alt.Scale(domain=regions, range=colors),
                scale=alt.Scale(domain=regions, scheme='category20'),
                title="Region",
            ),
            opacity=alt.condition(region_select, alt.value(1), alt.value(0.25)),
        )
    )
    .add_selection(region_select)
    .properties(title="Region Sales")
)
sales_data
region_summary = (
    (
        alt.Chart(sales_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "month(transaction_date)",
                type="temporal",
            ),
            y=alt.Y(
                field="transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Total Sales",
            ),
            color=alt.Color(
                "region",
                type="nominal",
                title="Regions",
                scale=alt.Scale(domain=regions, scheme='category20'),
                legend=alt.Legend(
                    direction="vertical",
                    symbolType="triangle-left",
                    tickCount=4,
                ),
            ),
        )
    )
    .transform_filter(region_select)
    .properties(width=400, title="Monthly Sales")
)

sellers_monthly_pie = (
    (
        alt.Chart(sales_data)
        .mark_arc(innerRadius=10)
        .encode(
            theta=alt.Theta(
                field="transaction_amount",
                type="quantitative",
                aggregate="sum",
                title="Total Transactions",
            ),
            color=alt.Color(
                "month(transaction_date)",
                type="temporal",
                title="Month",
                scale=alt.Scale(domain=months, scheme='category20'),
                legend=alt.Legend(
                    direction="vertical",
                    symbolType="triangle-left",
                    tickCount=12,
                ),
            ),
            facet=alt.Facet(
                field="seller",
                type="nominal",
                columns=4,
                title="Sellers",
            ),
            tooltip=alt.Tooltip(["sum(transaction_amount)", "month(transaction_date)"]),
        )
    )
    .transform_filter(region_select)
    .properties(width=100, height=100, title="Sellers transactions per month")
)

#top_row = region_pie | region_summary
full_chart =region_pie & region_summary & sellers_monthly_pie
st.altair_chart(full_chart)
#'''
