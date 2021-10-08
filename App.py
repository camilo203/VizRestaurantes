import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import openpyxl

st.set_page_config(page_title="Bocs", page_icon=r"https://res.cloudinary.com/camilo203/image/upload/v1633736859/Bocs2_3tonos_rokecf.png",layout="wide")

data = pd.read_excel(r"https://res.cloudinary.com/camilo203/raw/upload/v1633731092/Demo_zjvayc.xlsx",engine="openpyxl")

productos = data.Item.unique().tolist()
dias = data.Dia.unique().tolist()

producto = st.sidebar.multiselect("Seleccione los productos que desea ver:", productos, productos)

dia = st.sidebar.multiselect("Seleccione los dias que desea ver:", dias, dias)

genero = st.sidebar.multiselect("Seleccione el genero:", data.Genero.unique(), data.Genero.unique())

df_quer = data.query(
    "Genero == @genero & Dia == @dia & Item == @producto"
)


st.title(":bar_chart: Dashboard Negocio")
st.markdown("##")

#Indicadores
ventas_tot = int(data.Precio.sum())
edad_prom = int(data.Edad.mean())
mejor_cliente = data.groupby("Nombre").Precio.sum().sort_values().tail(1)

l_col, mid_col, r_col = st.columns(3)

with l_col:
    st.subheader("Ventas totales")
    st.subheader(f"COP $ {ventas_tot:,}")
with mid_col:
    st.subheader(f"Edad promedio de los clientes: {edad_prom} años")
with r_col:
    st.subheader("Cliente del mes")
    st.subheader(f"{mejor_cliente.index[0]} gasto COP ${mejor_cliente[0]:,}")

st.markdown("---")

#Ventas por producto
vProd = df_quer.groupby("Item").Precio.sum()
v_productos = px.bar(vProd, color_discrete_sequence=["#46AC95"]*len(producto))
v_productos.update_yaxes(title_text="Ventas")
v_productos.update_layout(showlegend=False)


#Ventas por dia

# df_quer.Dia = df_quer.Dia.apply(lambda x: pd.Categorical(x, ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"], ordered=True))
llave = {"Lunes":0, "Martes":1, "Miercoles":2, "Jueves":3, "Viernes":4, "Sabado":5}
porDia = df_quer.groupby("Dia").Precio.sum().to_frame()
porDia["Encrypt"] = porDia.index.to_series().apply(lambda x: llave[x])
porDia.sort_values(by="Encrypt",inplace=True)
barDia = px.bar(porDia.iloc[:,:1], color_discrete_sequence=["#46AC95"]*len(porDia["Precio"]))
barDia.update_yaxes(title_text="Ventas")
barDia.update_layout(showlegend=False)


#Top 5 Clientes

t5Clientes =df_quer.groupby(["Nombre"]).Precio.sum().sort_values(ascending=False).head(5)


lc, mc, rc = st.columns(3)

with lc:
    st.plotly_chart(v_productos, use_container_width=True)
with mc:
    st.plotly_chart(barDia, use_container_width=True)
with rc:
    t5Bar = px.bar(t5Clientes, color_discrete_sequence=["#46AC95"]*len(range(5)))
    t5Bar.update_layout(showlegend=False)
    st.plotly_chart(t5Bar, use_container_width=True)
#Genero Item

gItem = df_quer.groupby(["Genero", "Item"]).Precio.sum().to_frame().reset_index()
# st.dataframe(gItem.reset_index())


#Edad item

eItem = df_quer.groupby(["Edad", "Item"]).Precio.sum().to_frame().reset_index()
eIBar = px.bar(eItem, "Edad", "Precio", "Item", barmode="group")
eIBar.layout.xaxis.dtick = 1

lefc, rigc = st.columns(2)
with lefc:
    st.plotly_chart(px.bar(gItem, "Genero", "Precio", color="Item", barmode="group"), use_container_width=True)
with rigc:
    st.plotly_chart(eIBar, use_container_width=True)

# hide_st = """
#         <style>
#         #MainMenu {visibility: hidden;}
#         footer {visibility: hidden;}
#         header {visibility: hidden;}
#         </style>
#         """
# st.markdown(hide_st, unsafe_allow_html=True)

l, m, r = st.columns(3)

with m:
    button = st.button("Generar Reporte")

if button:
    st.markdown("[Descargue su reporte automatizado aqui:](https://www.google.com/)")



