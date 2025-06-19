
import streamlit as st
import pandas as pd

# Cargar los datos desde el CSV
df = pd.read_csv("ventas_los_gauchitos.csv", parse_dates=["fecha"])

st.set_page_config(page_title="Dashboard Los Gauchitos", layout="wide")
st.title("🌭 Dashboard de Los Gauchitos")
st.markdown("Análisis interactivo de **ventas, márgenes y rendimiento** por sucursal y producto.")

# Filtros
with st.sidebar:
    st.header("🔍 Filtros")
    sucursales = st.multiselect("Sucursal", df["sucursal"].unique(), default=df["sucursal"].unique())
    productos = st.multiselect("Producto", df["producto"].unique(), default=df["producto"].unique())
    fecha_min = df["fecha"].min().date()
    fecha_max = df["fecha"].max().date()
    fecha_rango = st.date_input("Rango de Fechas", (fecha_min, fecha_max))

# Aplicar filtros
df_filtrado = df[
    (df["sucursal"].isin(sucursales)) &
    (df["producto"].isin(productos)) &
    (df["fecha"].dt.date >= fecha_rango[0]) &
    (df["fecha"].dt.date <= fecha_rango[1])
]

# KPIs
margen_total = df_filtrado["margen"].sum()
venta_total = df_filtrado["venta_total"].sum()
costo_total = df_filtrado["costo_total"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Margen Total", f"Q{margen_total:,.2f}")
col2.metric("🛒 Ventas Totales", f"Q{venta_total:,.2f}")
col3.metric("📦 Costos Totales", f"Q{costo_total:,.2f}")

# Gráficas
st.subheader("📈 Margen por Día")
margen_dia = df_filtrado.groupby(df_filtrado["fecha"].dt.date)["margen"].sum()
st.line_chart(margen_dia)

st.subheader("🏆 Top 5 Productos por Margen")
top_productos = df_filtrado.groupby("producto")["margen"].sum().sort_values(ascending=False).head(5)
st.bar_chart(top_productos)

st.subheader("🏢 Margen por Sucursal")
margen_sucursal = df_filtrado.groupby("sucursal")["margen"].sum()
st.bar_chart(margen_sucursal)

# Tabla de datos
with st.expander("🔍 Ver datos filtrados"):
    st.dataframe(df_filtrado)
