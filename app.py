import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="PreparaCalda Pro", page_icon="🚜", layout="wide")

def conectar_banco():
    """Estabelece conexão com o banco de dados SQLite."""
    return sqlite3.connect('preparacalda2.db')

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown("""
    <style>
    .dosagem-box { 
        border: 1px solid #e6e6e6; 
        padding: 15px; 
        border-radius: 10px; 
        background-color: #f9f9f9; 
        margin-bottom: 10px; 
        min-height: 180px;
    }
    .stAlert { margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True) # <-- O ERRO ESTAVA AQUI, CORRIGIDO PARA unsafe_allow_html

st.title("🚜 PreparaCalda Pro")
st.subheader("Cálculo de Dosagem e Ordem de Mistura")

# --- CONEXÃO INICIAL ---
conn = conectar_banco()

# --- SIDEBAR: HISTÓRICO DE CONSULTAS ---
st.sidebar.header("🕒 Últimas Consultas")
try:
    df_logs = pd.read_sql("SELECT data_hora, protocolo_consultado FROM Logs_Consultas ORDER BY id_log DESC LIMIT 5", conn)
    for _, log in df_logs.iterrows():
        st.sidebar.write(f"📅 **{log['data_hora']}**")
        st.sidebar.caption(f"{log['protocolo_consultado']}")
        st.sidebar.markdown("---")
except:
    st.sidebar.info("O histórico aparecerá aqui após a primeira consulta.")

# --- ÁREA DE INPUT (CONFIGURAÇÃO) ---
with st.container():
    st.info("### 1. Configuração da Calda")
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Busca produtos para o menu de seleção
        query_produtos = "SELECT nome_comercial FROM Produtos ORDER BY nome_comercial"
        df_produtos = pd.read_sql(query_produtos, conn)
        
        selecionados = st.multiselect(
            "Selecione os produtos da mistura:",
            options=df_produtos['nome_comercial'].tolist(),
            help="Selecione todos os defensivos e fertilizantes que irá utilizar."
        )
    
    with col_b:
        volume_tanque = st.number_input("Volume total do tanque (Litros):", min_value=100, value=2000, step=100)

# --- ESPAÇO PARA DOSAGENS DINÂMICAS ---
dosagens_input = {}

if selecionados:
    st.write("### 2. Informe as Dosagens")
    cols = st.columns(3)
    
    for i, produto in enumerate(selecionados):
        with cols[i % 3]:
            # CORRIGIDO: de unsafe_allow_index para unsafe_allow_html
            st.markdown(f'<div class="dosagem-box">', unsafe_allow_html=True) 
            st.write(f"**{produto}**")
            
            if "Progibb" in produto:
                st.warning("⚠️ Item em Sachê (2,5g)")
                saches_por_1000 = st.number_input(f"Sachês p/ 1000L:", min_value=0.0, step=0.5, key=f"ds_{produto}")
                total_necessario = (saches_por_1000 / 1000) * volume_tanque
                dosagens_input[produto] = f"{total_necessario:.2f} sachês totais"
            else:
                dose_100l = st.number_input(f"Dose p/ 100L (ml ou g):", min_value=0.0, step=10.0, key=f"ds_{produto}")
                total_necessario = (dose_100l / 100) * volume_tanque
                dosagens_input[produto] = f"{total_necessario:.2f} (ml/g) totais"
            
            # CORRIGIDO: de unsafe_allow_index para unsafe_allow_html
            st.markdown('</div>', unsafe_allow_html=True)
    # --- BOTÃO DE PROCESSAMENTO ---
    if st.button("Gerar Protocolo Final"):
        st.markdown("---")
        st.write("### 📜 Protocolo de Preparo Passo a Passo")
        
        # 1. Alerta de Abastecimento Inicial (50% da água)
        agua_inicial = volume_tanque * 0.5
        st.warning(f"#### ⚠️ PASSO 0: ABASTECIMENTO INICIAL\n"
                   f"Encha o tanque com **{agua_inicial:.0f} Litros** de água (50% do volume) "
                   f"e mantenha a agitação ligada.")

        # 2. Busca e Ordenação Química
        placeholder = ', '.join(['?'] * len(selecionados))
        query_ordem = f"""
            SELECT p.nome_comercial, p.tipo_formulacao, c.nome_categoria, c.ordem_prioridade
            FROM Produtos p
            JOIN Categorias c ON p.id_categoria = c.id_categoria
            WHERE p.nome_comercial IN ({placeholder})
            ORDER BY c.ordem_prioridade ASC
        """
        
        df_res = pd.read_sql(query_ordem, conn, params=selecionados)
        
        # 3. Exibição dos Passos de Adição
        for idx, row in df_res.iterrows():
            nome = row['nome_comercial']
            tipo = row['tipo_formulacao'].upper() if row['tipo_formulacao'] else ""
            
            with st.expander(f"Passo {idx+1}: {nome}", expanded=True):
                st.success(f"**Adicionar {dosagens_input[nome]}**")
                
                # Alerta de Pré-diluição para produtos sólidos
                if tipo in ['WP', 'WG', 'SG', 'PÓ', 'PÓ MOLHÁVEL', 'FERT PO']:
                    st.error(f"💡 **CUIDADO:** Este produto é uma formulação sólida ({tipo}). "
                             "É obrigatório fazer a **pré-diluição** em um balde com água antes de colocar no tanque.")
                
                st.caption(f"Formulação: {tipo} | Categoria: {row['nome_categoria']}")

        # 4. Alerta de Finalização
        st.info(f"#### ✅ PASSO FINAL: COMPLETAR VOLUME\n"
                f"Após a adição de todos os itens, complete o tanque com água até atingir os **{volume_tanque} Litros**.")

        # --- SALVAR NO HISTÓRICO (LOG) ---
        try:
            cursor = conn.cursor()
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
            protocolo_texto = " + ".join(selecionados)
            cursor.execute("INSERT INTO Logs_Consultas (data_hora, protocolo_consultado) VALUES (?, ?)", 
                           (data_atual, protocolo_texto))
            conn.commit()
            st.toast("Consulta salva no histórico!")
        except Exception as e:
            st.error(f"Erro ao salvar histórico: {e}")

conn.close()