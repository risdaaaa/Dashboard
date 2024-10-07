import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import streamlit as st



sns.set(style='whitegrid')

# Cache for creating daily orders DataFrame
@st.cache_data
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_approved_at').agg({
        "order_id": "nunique",
        "payment_value": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "payment_value": "revenue"
    }, inplace=True)
    return daily_orders_df

@st.cache_data
def create_sum_order_items_df(df):
    sum_order_items_df = df.groupby("product_category_name_english")['payment_value'].sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

@st.cache_data
def create_sum_order_items_by_order_id_df(df):
    sum_order_items_df = df.groupby("product_category_name_english")['order_id'].nunique().sort_values(ascending=False).reset_index()
    sum_order_items_df.rename(columns={"order_id": "total_orders"}, inplace=True)
    return sum_order_items_df

@st.cache_data
def create_bystate_df(df):
    bystate_df = df.groupby('customer_state').agg(
        customer_count=('customer_id', 'nunique'),
        seller_count=('seller_id', 'nunique')
    ).reset_index()
    bystate_df.columns = ['state', 'customer_count', 'seller_count']
    return bystate_df

@st.cache_data
def create_rfm_df(df, recent_date):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_approved_at": "max",
        "order_id": "nunique",
        "payment_value": "sum"
    })

    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df

# Cache for loading the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("all_data.csv")
    datetime_columns = ["order_approved_at",
                        "order_delivered_customer_date",
                        "order_delivered_carrier_date",
                        "order_estimated_delivery_date"]
    df.sort_values(by="order_approved_at", inplace=True)
    for column in datetime_columns:
        df[column] = pd.to_datetime(df[column], errors='coerce')
    return df

# Load the dataset
df = load_data()

# Calculate recent_date from the full dataset (before applying the filter)
recent_date = df["order_approved_at"].max()

# Streamlit sidebar for filtering by date range
min_date = df["order_approved_at"].min()
max_date = df["order_approved_at"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/risdaaaa/Dashboard/refs/heads/main/logo.jpg")
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter the dataset based on the selected date range
main_df = df[(df["order_approved_at"] >= str(start_date)) & 
              (df["order_approved_at"] <= str(end_date))]

# Create cached dataframes using the filtered data
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
sum_order_items_by_order_id_df = create_sum_order_items_by_order_id_df(main_df)
bystate_df = create_bystate_df(main_df)

# Create the RFM dataframe using the filtered data but with the recent_date based on the full dataset
rfm_df = create_rfm_df(main_df, recent_date)

#=====================================================================================================================
st.markdown("<h1 style='text-align: center;'>MY E-Commerce Dashboard!</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: none; height: 2px; background-color: black;'>", unsafe_allow_html=True)
#=====================================================================================================================
# Daily Orders
st.header('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "BRL", locale='pt_BR') 
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_approved_at"],
    daily_orders_df["order_count"],
    marker='o', 
    linewidth=2,
    color="#3A6D8C"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

#=========================================================================================================================================
# Product
st.header("Best and Worst Performing Product")

# Warna
blue = '#8EACCD'
green = '#D2E0FB'
colors = [blue, green, green, green, green]

# Menghitung jumlah produk yang terjual per kategori
product_sales = df.groupby('product_category_name_english')['order_id'].count().reset_index()
product_sales.columns = ['product_category_name_english', 'total_sold']
product_sales = product_sales.sort_values(by='total_sold', ascending=False)

# Membuat subplots
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))

# Produk dengan penjualan terbanyak
sns.barplot(x="total_sold", y="product_category_name_english", 
            data=product_sales.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Best Performing Product", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

# Menambahkan label nilai pada batang
for i in ax[0].patches:
    ax[0].text(i.get_width() + 0.2, i.get_y() + i.get_height() / 2, 
               f'{int(i.get_width())}', ha='right', va='center', fontsize=12, color='black', weight='bold')

# Produk dengan penjualan paling sedikit
sns.barplot(x="total_sold", y="product_category_name_english", 
            data=product_sales.sort_values(by="total_sold", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()  # Membalikkan sumbu x
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()  # Memindahkan label sumbu y ke kanan
ax[1].set_title("Worst Performing Product", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

# Menambahkan label nilai pada batang
for i in ax[1].patches:
    ax[1].text(i.get_width() - 0.2, i.get_y() + i.get_height() / 2, 
               f'{int(i.get_width())}', ha='left', va='center', fontsize=12, color='black', weight='bold')

st.pyplot(fig)

#================================================================================================================================
# Adding the new pie chart for review scores
st.header("Our Ratings by Customers")

# Group by 'review_score' and sort by the count in descending order
review_score_counts = df.groupby('review_score')['order_id'].count().sort_values(ascending=False)

# Warna
colors = ['#3A6D8C', '#C4D7FF','#8EACCD', '#6A9AB0', '#D2E0FB']

# Membuat pie chart
plt.figure(figsize=(8, 8))
plt.pie(review_score_counts, labels=review_score_counts.index, autopct='%1.1f%%', 
        startangle=90, colors=colors)

# Menambahkan judul
plt.title('Customer Satisfaction Based on Product Review Score', fontsize=16)

# Menambahkan legend di luar pie chart agar tidak memotong
plt.legend(
    labels=[f'Score {score}: {count}' for score, count in zip(review_score_counts.index, review_score_counts)],
    loc='center left', 
    bbox_to_anchor=(1, 0.5),  # Memindahkan legend ke samping
    fontsize=12
)

# Display the pie chart
st.pyplot(plt)
#=================================================================================================================================
#Payment
st.header("Payment Distribution")
payment_method = df['payment_type'].value_counts().reset_index()
payment_method.columns = ['payment_type', 'count']

# Warna 
colors = ['#3A6D8C', '#D2E0FB', '#D2E0FB', '#D2E0FB', '#D2E0FB']

# Membuat diagram batang
plt.figure(figsize=(20, 8))
sns.barplot(x='count', y='payment_type', data=payment_method, palette=colors)

# Menambahkan label dan judul
plt.xlabel('Frequency of Payment Method', fontsize=16)
plt.ylabel('Payment Type', fontsize=16)
plt.title('Frequency of Transaction by Payment Type', fontsize=16)

# Menambahkan label nilai pada batang
for i in plt.gca().patches:
    plt.gca().text(i.get_width() + 0.2, i.get_y() + i.get_height() / 2, 
                   f'{int(i.get_width())}', ha='left', va='center', fontsize=12, color='black')


st.pyplot(plt)
#=================================================================================================================================
# Customer & Seller Distribution
st.header("Our Customers and Sellers")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 8))

colors = ['#8EACCD' if i == 0 else '#D2E0FB' for i in range(len(bystate_df))]

sns.barplot(
    x="customer_count", 
    y="state", 
    data=bystate_df.sort_values(by="customer_count", ascending=False).head(5),
    palette=colors, 
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("States with Most Customers", loc="center", fontsize=18)
ax[0].tick_params(axis='y', labelsize=15)

for i in ax[0].patches:
    ax[0].text(i.get_width() + 0.2, i.get_y() + i.get_height()/2, 
               f'{int(i.get_width())}', ha='left', va='center', fontsize=12, color='black', weight='bold')

sns.barplot(
    x="seller_count", 
    y="state", 
    data=bystate_df.sort_values(by="seller_count", ascending=False).head(5),
    palette=colors, 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("States with Most Sellers", loc="center", fontsize=18)
ax[1].tick_params(axis='y', labelsize=15)

for i in ax[1].patches:
    ax[1].text(i.get_width() - 0.2, i.get_y() + i.get_height()/2, 
               f'{int(i.get_width())}', ha='right', va='center', fontsize=14, color='black', weight='bold')

st.pyplot(fig)

#====================================================================================================================

# Streamlit subheader for RFM metrics
st.header("Best Customer Based on RFM Parameters")

# Displaying the RFM summary metrics
col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    # Formatting for Brazilian Real (BRL)
    avg_monetary = format_currency(rfm_df.monetary.mean(), "BRL", locale='pt_BR')
    st.metric("Average Monetary", value=avg_monetary)

# Mengambil 5 karakter customer_id di awal
rfm_df['short_customer_id'] = rfm_df['customer_id'].apply(lambda x: x[:5])  

# Plotting with shortened customer_id
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(30, 6))

colors = ["#8EACCD", "#8EACCD", "#8EACCD", "#8EACCD", "#8EACCD"]

sns.barplot(y="recency", x="short_customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=18)
ax[0].tick_params(axis ='x', labelsize=15)

sns.barplot(y="frequency", x="short_customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=18)
ax[1].tick_params(axis='x', labelsize=15)

sns.barplot(y="monetary", x="short_customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=18)
ax[2].tick_params(axis='x', labelsize=15)

for axis in ax:
    axis.tick_params(axis='x', rotation=45)

# Display the plot in Streamlit
st.pyplot(fig)
st.caption('Copyright (c) risdew 2024')


