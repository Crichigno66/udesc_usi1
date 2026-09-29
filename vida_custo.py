import streamlit as st
import numpy as np
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Simulador VB - Ensaios de Usinagem", layout="wide")

# --- LISTA PRÉ-DEFINIDA DE ALUNOS ---
LISTA_ALUNOS = [
    "Selecione seu nome...",
    "Alexandre",
    "Arthur G.",
    "Arthur S.",
    "Eduardo",
    "João"
]

# --- ESTRUTURA DE MEMÓRIA (Guarda o histórico individual de cada aluno) ---
if "banco_dados_alunos" not in st.session_state:
    # Dicionário onde a chave é o nome do aluno e o valor é a lista de ensaios dele
    st.session_state.banco_dados_alunos = {aluno: [] for aluno in LISTA_ALUNOS if aluno != "Selecione seu nome..."}


# --- FUNÇÃO DE CÁLCULO DE VB COM RUÍDO (±10%) ---
def calcular_desgaste_vb(vc, f, ap, t):
    K = 1.185e-6
    x, y, z = 2.128, 0.724, 0.388
    
    vb_teorico = K * (vc ** x) * (f ** y) * (ap ** z) * t
    fator_ruido = np.random.uniform(0.90, 1.10)
    
    return vb_teorico * fator_ruido


# --- INTERFACE PRINCIPAL ---
st.title("Simulador de Desgaste da Ferramenta (VB) — Coeficientes de Taylor")

st.markdown("""
**Instruções para o Ensaio:**
Selecione seu nome na lista abaixo antes de realizar as medições. 
Cada ensaio gerado consome insumos de laboratório e **o custo operacional aumenta exponencialmente a cada novo experimento**. 
Não é possível reiniciar o histórico de ensaios acumulados.
""")

# Seleção de Aluno via Dropdown
aluno_selecionado = st.selectbox("Selecione seu Nome / Matrícula:", LISTA_ALUNOS)

st.divider()

# Só exibe o simulador após a seleção de um aluno válido
if aluno_selecionado != "Selecione seu nome...":
    
    # Recupera o histórico do aluno selecionado
    historico_aluno = st.session_state.banco_dados_alunos[aluno_selecionado]
    
    # --- ENTRADA DE PARÂMETROS ---
    st.subheader("⚙️ Condições de Corte")

    col1, col2 = st.columns(2)

    with col1:
        vc = st.number_input(
            "Velocidade de Corte - v_c (m/min)",
            min_value=1.0, max_value=500.0, value=120.0, step=5.0, format="%.1f"
        )
        f = st.number_input(
            "Avanço - f (mm/rot)",
            min_value=0.01, max_value=2.00, value=0.20, step=0.01, format="%.2f"
        )

    with col2:
        ap = st.number_input(
            "Profundidade de Corte - a_p (mm)",
            min_value=0.1, max_value=10.0, value=1.5, step=0.1, format="%.1f"
        )
        t = st.number_input(
            "Tempo de Usinagem - t (min)",
            min_value=0.1, max_value=180.0, value=10.0, step=1.0, format="%.1f"
        )

    # --- CÁLCULO DE CUSTO EXPONENCIAL ---
    n_ensaio = len(historico_aluno) + 1
    custo_ensaio_atual = 1500.0 * (1.35 ** (n_ensaio - 1))

    st.info(f"💡 Custo previsto para realizar o **Ensaio nº {n_ensaio}**: **R$ {custo_ensaio_atual:.2f}**")

    # --- BOTÃO PARA EXECUTAR MEDIÇÃO ---
    if st.button("🧪 Realizar Medição e Registrar Ensaio", type="primary"):
        vb_calculado = calcular_desgaste_vb(vc, f, ap, t)
        
        # Salva o resultado diretamente no repositório do aluno
        historico_aluno.append({
            "Ensaio nº": n_ensaio,
            "v_c (m/min)": vc,
            "f (mm/rot)": f,
            "a_p (mm)": ap,
            "Tempo t (min)": t,
            "VB Medido (mm)": round(vb_calculado, 4),
            "Custo do Ensaio (R$)": round(custo_ensaio_atual, 2)
        })
        st.success(f"Ensaio nº {n_ensaio} registrado para {aluno_selecionado}!")
        st.rerun()

    st.divider()

    # --- EXIBIÇÃO DOS RESULTADOS ---
    st.subheader(f"📊 Histórico e Orçamento — Aluno: {aluno_selecionado}")

    if historico_aluno:
        df_historico = pd.DataFrame(historico_aluno)
        
        ultimo_vb = df_historico.iloc[-1]["VB Medido (mm)"]
        custo_acumulado = df_historico["Custo do Ensaio (R$)"].sum()
        
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric(label="Último Desgaste Medido (VB)", value=f"{ultimo_vb:.3f} mm")
        with col_m2:
            st.metric(label="Total de Ensaios Realizados", value=len(df_historico))
        with col_m3:
            st.metric(label="Custo Total Acumulado", value=f"R$ {custo_acumulado:,.2f}")

        if ultimo_vb >= 0.3:
            st.warning("⚠️ Critério de fim de vida da ferramenta atingido na última medição (VB >= 0.3 mm).")

        st.markdown("### Tabela de Dados Coletados")
        st.dataframe(df_historico, use_container_width=True)

        # Apenas botão de download (sem botão de reiniciar)
        nome_arquivo = f"ensaios_taylor_{aluno_selecionado.replace(' ', '_')}.csv"
        csv_data = df_historico.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Baixar Tabela de Dados (CSV)",
            data=csv_data,
            file_name=nome_arquivo,
            mime="text/csv"
        )
    else:
        st.info("Nenhum ensaio registrado para este aluno ainda.")

else:
    st.warning("⚠️ Por favor, selecione seu nome na caixa acima para acessar o simulador.")
