import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =========================
# 1. CARGA DE DATOS
# =========================
df = pd.read_csv("data/zapatillas.csv")

print("Primeras filas:")
print(df.head())

print("\nInformación general:")
print(df.info())

# =========================
# 2. LIMPIEZA DE DATOS
# =========================

# convertir fecha
df["order_date"] = pd.to_datetime(df["order_date"])

# crear columna temporal (año-mes)/(mes)
#df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
df["month"] = df["order_date"].dt.month_name()
month_order = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# comprobar nulos
print("\nValores nulos por columna:")
print(df.isnull().sum())

# comprobar duplicados
print("\nFilas duplicadas:", df.duplicated().sum())

# comprobar tipos finales
print("\nTipos de datos:")
print(df.dtypes)

# =========================
# 3. KPIs BÁSICOS
# =========================
print("\n===== KPIs =====")

print("Ingresos totales:", df["revenue_usd"].sum())
print("Ventas totales:", df["units_sold"].sum())
print("Ticket medio:", df["revenue_usd"].mean())
print("Precio medio:", df["final_price_usd"].mean())

# =========================
# 4. PRIMERAS AGRUPACIONES
# =========================

print("\nIngresos por marca:")
print(df.groupby("brand")["revenue_usd"].sum().sort_values(ascending=False))

print("\nIngresos por país:")
print(df.groupby("country")["revenue_usd"].sum().sort_values(ascending=False))

print("\nVentas por género:")
print(df.groupby("gender")["units_sold"].sum().sort_values(ascending=False))

# =========================
# 5. ANÁLISIS EXPLORATORIO
# =========================

print("\n===== ANÁLISIS EXPLORATORIO =====")

# Top marcas por ingresos
top_brands = df.groupby("brand")["revenue_usd"].sum().sort_values(ascending=False)
print("\nTop marcas por ingresos:")
print(top_brands)

# Top categorías por ingresos
top_categories = df.groupby("category")["revenue_usd"].sum().sort_values(ascending=False)
print("\nTop categorías por ingresos:")
print(top_categories)

# Top países por ingresos
top_countries = df.groupby("country")["revenue_usd"].sum().sort_values(ascending=False)
print("\nTop países por ingresos:")
print(top_countries)

# Ventas por género
sales_gender = df.groupby("gender")["units_sold"].sum().sort_values(ascending=False)
print("\nVentas por género:")
print(sales_gender)

# Ventas por canal
sales_channel = df.groupby("sales_channel")["units_sold"].sum().sort_values(ascending=False)
print("\nVentas por canal:")
print(sales_channel)

# Ventas por método de pago
sales_payment = df.groupby("payment_method")["units_sold"].sum().sort_values(ascending=False)
print("\nVentas por método de pago:")
print(sales_payment)



# =========================
# 6. VISUALIZACIÓN
# =========================
"""
# Ingresos por marca
brand_revenue = df.groupby("brand")["revenue_usd"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
brand_revenue.plot(kind="bar")

plt.title("Ingresos por Marca")
plt.xlabel("Marca")
plt.ylabel("Ingresos (USD)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# Ventas por género
gender_sales = df.groupby("gender")["units_sold"].sum()

plt.figure(figsize=(8, 8))
plt.pie(
    gender_sales,
    labels=gender_sales.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Ventas por Género")
plt.tight_layout()

plt.show()"""



# preparar datos
brand_revenue = df.groupby("brand")["revenue_usd"].sum().sort_values(ascending=False)
gender_sales = df.groupby("gender")["units_sold"].sum()
channel_sales = df.groupby("sales_channel")["units_sold"].sum()
payment_sales = df.groupby("payment_method")["units_sold"].sum()
#monthly_revenue = df.groupby("year_month")["revenue_usd"].sum()
monthly_revenue = df.groupby("month")["revenue_usd"].sum().reindex(month_order)
category_sales = df.groupby("category")["units_sold"].sum().sort_values(ascending=False)

# crear layout de gráficos
fig, axes = plt.subplots(
    3, 2,
    figsize=(16, 12),
    gridspec_kw={"height_ratios": [1.2, 1, 1.2]}
)

# -------------------------     
# 1. Ingresos por marca
# -------------------------
brand_revenue.plot(kind="bar", ax=axes[0, 0])
axes[0, 0].set_title("Ingresos por Marca")
axes[0, 0].set_xlabel("Marca")
axes[0, 0].set_ylabel("Ingresos (USD)")
axes[0, 0].tick_params(axis="x", rotation=45)
axes[0, 0].set_title("Ingresos por Marca", fontsize=14)

# -------------------------
# 2. Ventas por género
# -------------------------
axes[0, 1].pie(
    gender_sales,
    labels=gender_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[0, 1].set_title("Ventas por Género")

# -------------------------
# 3. Canal de venta
# -------------------------
axes[1, 0].pie(
    channel_sales,
    labels=channel_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1, 0].set_title("Canal de Venta")

# -------------------------
# 4. Método de pago
# -------------------------
axes[1, 1].pie(
    payment_sales,
    labels=payment_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
axes[1, 1].set_title("Método de Pago")

# -------------------------
# 5. Evolución temporal
# -------------------------
axes[2, 0].plot(monthly_revenue.index, monthly_revenue.values, marker="o")
axes[2, 0].set_title("Evolución de Ingresos por Mes")
axes[2, 0].set_xlabel("Mes")
axes[2, 0].set_ylabel("Ingresos (USD)")
axes[2, 0].tick_params(axis="x", rotation=45)

# -------------------------
# 6. Tipo de zapatilla más vendida
# -------------------------
category_sales.plot(kind="bar", ax=axes[2, 1])
axes[2, 1].set_title("Tipo de Zapatilla Más Vendida")
axes[2, 1].set_xlabel("Categoría")
axes[2, 1].set_ylabel("Unidades Vendidas")
axes[2, 1].tick_params(axis="x", rotation=45)

# layout final
plt.tight_layout()
plt.show()
plt.subplots_adjust(hspace=0.6, wspace=0.25)

# =========================
# 7. HEATMAP PAÍS x CATEGORÍA
# =========================

pivot_country_category = df.pivot_table(
    values="revenue_usd",
    index="country",
    columns="category",
    aggfunc="sum"
)

plt.figure(figsize=(10, 6))

sns.heatmap(
    pivot_country_category,
    annot=True,
    fmt=".0f",
    cmap="Blues"
)

plt.title("Ingresos por País y Categoría")
plt.xlabel("Categoría")
plt.ylabel("País")

plt.tight_layout()
plt.show()


# =========================
# 8. INSIGHTS CLAVE
# =========================

print("\n===== INSIGHTS CLAVE =====")

top_brand = df.groupby("brand")["revenue_usd"].sum().idxmax()
top_country = df.groupby("country")["revenue_usd"].sum().idxmax()
top_gender = df.groupby("gender")["units_sold"].sum().idxmax()
top_channel = df.groupby("sales_channel")["units_sold"].sum().idxmax()
top_payment = df.groupby("payment_method")["units_sold"].sum().idxmax()
top_month = df.groupby("month")["revenue_usd"].sum().reindex(month_order).idxmax()
top_category = df.groupby("category")["units_sold"].sum().idxmax()

print(f"- La marca con mayor facturación es {top_brand}.")
print(f"- El país con más ingresos es {top_country}.")
print(f"- El segmento con más ventas es {top_gender}.")
print(f"- El canal dominante es {top_channel}.")
print(f"- El método de pago más usado es {top_payment}.")
print(f"- El mes con más ingresos es {top_month}.")
print(f"- La categoría más vendida es {top_category}.")


print("\nFIN DEL SCRIPT")

