import streamlit as st
import pandas as pd

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
if selected_brands and "Todas" not in selected_brands:
    filtered_df = filtered_df[filtered_df["brand"].isin(selected_brands)]

# País
if selected_countries and "Todos" not in selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

# Categoría
if selected_categories and "Todas" not in selected_categories:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

# Género
if selected_genders and "Todos" not in selected_genders:
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

# Preview
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20))