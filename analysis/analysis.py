import pandas as pd

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

# crear columna temporal (año-mes)
df["year_month"] = df["order_date"].dt.to_period("M").astype(str)

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