import streamlit as st
import pandas as pd
import json
import datetime
from funcoes import carregar_metas, salvar_metas

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

    col_tabela, col_cards = st.columns([3,1])
    # -------------------
    # tabela
    # -------------------
    with col_tabela:
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
    # cards
    # -------------------
    with col_cards:
       with st.container(border=True):
        st.subheader("Resumo")
        
        total = df["valor"].sum()
        qtd = len(df)
        media = df["valor"].mean() if qtd > 0 else 0
        maior = df["valor"].max() if qtd > 0 else 0
        
        def card(titulo, valor):
            st.markdown(f"""
            <div style="
                padding:19px;
                border-radius:10px;
                background-color:#111;
                margin-bottom:10px;
            ">
                <div style="font-size:12px; color:gray;">{titulo}</div>
                <div style="font-size:18px; font-weight:bold;">{valor}</div>
            </div>
            """, unsafe_allow_html=True)
        
        card("💰 Total", f"R$ {total:.2f}")
        card("📊 Média", f"R$ {media:.2f}")
        card("🧾 Quantidade", qtd)
        card("🚨 Maior gasto", f"R$ {maior:.2f}")
    
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
    
     # -------------------
    # metas
    # -------------------
    st.subheader("🎯 Definir metas por categoria")
    
    metas = carregar_metas()
    
    categorias = df["categoria"].unique() if not df.empty else []
    
    for cat in categorias:
        valor_meta = st.number_input(
            f"Meta para {cat} ",
            min_value=0.0,
            value=None,
            key=f"meta_{cat}"   
        )
        
        metas[cat] = valor_meta
        
    if valor is None:
        st.warning("Digite um valor!")
        st.stop()
    
    if st.button("Salvar metas"):
        salvar_metas(metas)
        st.success("Metas salvas!")
        st.rerun()
        
    # -------------------
    # controle de metas
    # -------------------
    st.subheader("📊 Controle de metas")
    
    metas = carregar_metas()
    
    for cat, total in por_categoria.items():
        limite = metas.get(cat)
        
        if limite and limite > 0:
            porcentagem = (total / limite) * 100
            progresso = min(total / limite, 1.0)
            
            if porcentagem >= 100:
                st.error(f"{cat}: R$ {total:.2f} / R$ {limite:.2f} (Estourou!)")
            elif porcentagem >= 80:
                st.warning(f"{cat}: R$ {total:.2f} / R$ {limite:.2f} (Atenção!)")
            else:
                st.success(f"{cat}: R$ {total:.2f} / R$ {limite:.2f}")
                
            st.progress(progresso)
    
    
else:
    st.info("Nenhum gasto cadastrado ainda.")

