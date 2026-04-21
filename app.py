import streamlit as st
import pandas as pd
import json

#carregar dados
with open("gastos.json", "r") as arquivo:
    gastos = json.load(arquivo)
    
df = pd.DataFrame(gastos)

#extrair mês

df["mes"] = df["data"].str[:7]

st.title(" 💰 Controle de Gastos")

#tabela
st.subheader("Seus gastos")
st.dataframe(df)

#total geral
total = df["valor"].sum()
st.metric("Total gasto", f"R$ {total:.2f}")

#gastos por categoria
st.subheader("Gastos por categoria")

por_categoria = df.groupby("categoria")["valor"].sum()

st.bar_chart(por_categoria)

#gastos por mes
st.subheader("Gastos por mês")

por_mes = df.groupby("mes")["valor"].sum()

st.line_chart(por_mes)

#filtro por mes(interativo)
st.subheader("Filtrar por mês")

meses = df["mes"].unique()
mes_selecionado = st.selectbox("Escolha o mês", meses)

df_filtrado = df[df["mes"] == mes_selecionado]

st.dataframe(df_filtrado)
st.write("Total:", df_filtrado["valor"].sum()) 

