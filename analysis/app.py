import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------
# Config
# -------------------------

st.set_page_config(page_title="Sneaker Sales Dashboard", layout="wide")

# -------------------------
# Load data
# -------------------------

df = pd.read_csv("data/zapatillas.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.month_name()


#-------------------------
# Sidebar Filters
# -------------------------

st.sidebar.caption("Si no seleccionas nada, se muestran todos los datos")
st.sidebar.header("Filtros")

# Marca
selected_brands = st.sidebar.multiselect(
    "Marca",
    options=sorted(df["brand"].unique())
)

# País
selected_countries = st.sidebar.multiselect(
    "País",
    options=sorted(df["country"].unique())
)

# Categoría
selected_categories = st.sidebar.multiselect(
    "Categoría",
    options=sorted(df["category"].unique())
)

# Género
selected_genders = st.sidebar.multiselect(
    "Género",
    options=sorted(df["gender"].unique())
)

# Fecha (rango)
min_date = df["order_date"].min()
max_date = df["order_date"].max()

selected_dates = st.sidebar.date_input(
    "Rango de fechas",
    [min_date, max_date]
)

# -------------------------
# Data filtering
# -------------------------
filtered_df = df.copy()

# Marca
if selected_brands:
    filtered_df = filtered_df[filtered_df["brand"].isin(selected_brands)]

# País
if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

# Categoría
if selected_categories:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

# Género
if selected_genders:
    filtered_df = filtered_df[filtered_df["gender"].isin(selected_genders)]

# Filtro fechas
if len(selected_dates) == 2:
    start_date = pd.to_datetime(selected_dates[0])
    end_date = pd.to_datetime(selected_dates[1])

    filtered_df = filtered_df[
        (filtered_df["order_date"] >= start_date) &
        (filtered_df["order_date"] <= end_date)
    ]

# -------------------------
# Data aggregations
# -------------------------

brand_revenue = filtered_df.groupby("brand")["revenue_usd"].sum().sort_values(ascending=False)

gender_sales = filtered_df.groupby("gender")["units_sold"].sum()

channel_sales = filtered_df.groupby("sales_channel")["units_sold"].sum()

payment_sales = filtered_df.groupby("payment_method")["units_sold"].sum()

monthly_revenue = (
    filtered_df
    .groupby(filtered_df["order_date"].dt.to_period("M"))["revenue_usd"]
    .sum()
    .sort_index()
)

category_sales = filtered_df.groupby("category")["units_sold"].sum().sort_values(ascending=False)

# -------------------------
# Title
# -------------------------

st.title("👟 Sneaker Sales Dashboard")
st.markdown("Interactive analytics dashboard for sneaker sales performance.")

# -------------------------
# KPIs
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${filtered_df['revenue_usd'].sum():,.0f}")
col2.metric("Units Sold", f"{filtered_df['units_sold'].sum():,}")
col3.metric("Avg Ticket", f"${filtered_df['revenue_usd'].mean():.2f}")

st.subheader("📊 Análisis de Ventas")


#-------------------------
# Gráficos
#-------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("Ingresos por Marca")
    st.bar_chart(brand_revenue)

with col2:
    st.subheader("Ventas por Género")

    fig, ax = plt.subplots(figsize=(4, 4))

    ax.pie(
        gender_sales,
        labels=None,
        autopct="%1.1f%%"
    )

    ax.legend(gender_sales.index)

    st.pyplot(fig)
    plt.close(fig)

    
col3, col4 = st.columns(2)

with col3:
    st.subheader("Canal de Venta")

    fig, ax = plt.subplots(figsize=(4, 4))

    ax.pie(
        channel_sales,
        labels=None,
        autopct="%1.1f%%"
    )

    ax.legend(channel_sales.index)
    st.pyplot(fig)
    plt.close(fig)

with col4:
    st.subheader("Método de Pago")

    fig, ax = plt.subplots(figsize=(4, 4))

    ax.pie(
        payment_sales,
        labels=None,
        autopct="%1.1f%%"
    )

    ax.legend(payment_sales.index)
    st.pyplot(fig)
    plt.close(fig)


col5, col6 = st.columns(2)

with col5:
    st.subheader("Evolución de Ingresos")
    st.line_chart(monthly_revenue)

with col6:
    st.subheader("Categoría Más Vendida")
    st.bar_chart(category_sales)    

if filtered_df.empty:
    st.warning("No hay datos con los filtros seleccionados")
    st.stop()

# Preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))

