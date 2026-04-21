import streamlit as st
import pandas as pd
import json
import datetime

st.title(" 💰 Controle de Gastos") 

#--------------
#carregar dados
#--------------
try:
    with open("gastos.json", "r") as arquivo:
        gastos = json.load(arquivo)
except:
    gastos = []
    
df = pd.DataFrame(gastos)
    
# estado
if "abrir_form" not in st.session_state:
    st.session_state.abrir_form = False

if "sucesso" not in st.session_state:
    st.session_state.sucesso = False

# mensagem persistente
if st.session_state.get("sucesso"):
    st.success("✅ Gasto adicionado!")
    st.session_state.sucesso = False

# expander
with st.expander("➕ Adicionar gasto", expanded=False):

    with st.form("form_gasto", clear_on_submit=True):
        nome = st.text_input("Nome")
        valor = st.number_input(
            "Valor",
            min_value=0.0,
            format="%.2f",
            value=None,
            placeholder="Digite o valor"
        )
        categoria = st.text_input("Categoria")
        data = st.date_input("Data", value=datetime.date.today())

        enviado = st.form_submit_button("Salvar")
        
        if enviado: 
            
            #validação
            if not nome or valor is None or not categoria:
                st.warning("Preencha todos os campos!")
                st.stop()

            novo_gasto = {
                "nome": nome,
                "valor": valor,
                "categoria": categoria,
                "data": data.strftime("%Y-%m-%d")
            }

            gastos.append(novo_gasto)

            with open("gastos.json", "w") as arquivo:
                json.dump(gastos, arquivo, indent=4)

            # controle
            st.session_state.sucesso = True
            st.rerun()
# -------------------
# dataframe
# -------------------        

if not df.empty:
    df["mes"] = df["data"].str[:7]

    # -------------------
    # tabela
    # -------------------
    st.subheader("📋 Seus gastos")
    edited_df = st.data_editor(df, num_rows="dynamic")
    
    if st.button("💾 Salvar alterações"):
        
        novos_gastos = edited_df.to_dict(orient="records")
        
        with open("gastos.json", "w") as arquivo:
            json.dump(novos_gastos, arquivo, indent=4)
            
        st.success("Alterações salvas!")
        st.rerun()

    # -------------------
    # total geral
    # -------------------
    total = df["valor"].sum()
    st.metric("Total gasto", f"R$ {total:.2f}")

    # -------------------
    # gráfico categoria
    # -------------------
    st.subheader("📊 Gastos por categoria")

    por_categoria = df.groupby("categoria")["valor"].sum()

    st.bar_chart(por_categoria)

    # -------------------
    # gráfico mês
    # -------------------
    st.subheader("📅 Gastos por mês")

    por_mes = df.groupby("mes")["valor"].sum()

    st.line_chart(por_mes)

    # -------------------
    # filtro
    # -------------------
    st.subheader("🔎 Filtrar por mês")

    meses = df["mes"].unique()
    mes_selecionado = st.selectbox("Escolha o mês", meses)

    df_filtrado = df[df["mes"] == mes_selecionado]

    st.dataframe(df_filtrado)
    st.write(f"Total: R$ {df_filtrado['valor'].sum():.2f}")
    
else:
    st.info("Nenhum gasto cadastrado ainda.")

