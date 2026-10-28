import streamlit as st
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Cálculo de Custo de Usinagem",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Cálculo de Custo de Usinagem (Exemplo 13.2 DeVries)")
st.markdown("Ferramenta para estimativa econômica e otimização de parâmetros de corte em operações de torneamento.")

# ==========================================
# BARRA LATERAL - ENTRADAS DE DADOS
# ==========================================
st.sidebar.header("📥 Parâmetros de Entrada")

# 1. Informações da Peça
st.sidebar.subheader("1. Geometria da Peça")
D = st.sidebar.number_input("Diâmetro da peça (D) [mm]", value=70.0, step=1.0)
L = st.sidebar.number_input("Comprimento usinado (L) [mm]", value=200.0, step=5.0)

# 2. Condições de Usinagem
st.sidebar.subheader("2. Condições de Corte")
#N = st.sidebar.number_input("Rotação da árvore (N) [rpm]", value=700.0, step=50.0)
V = st.sidebar.number_input("Velocidade de corte (vc) [m/min]", value=160.0, step=10.0)
f = st.sidebar.number_input("Avanço (f) [mm/volta]", value=0.3, step=0.05, format="%.2f")
Le = st.sidebar.number_input("Distância de aproximação (Le) [mm]", value=2.0, step=0.5)
Lx = st.sidebar.number_input("Distância de retorno/recuo (Lx) [mm]", value=80.0, step=5.0)

# 3. Informações da Ferramenta
st.sidebar.subheader("3. Ferramenta de Corte")
C1 = st.sidebar.number_input("Constante de Taylor (C1)", value=500.0, step=10.0)
n_taylor = st.sidebar.number_input("Expoente de Taylor (n)", value=0.25, step=0.01, format="%.2f")
C_t = st.sidebar.number_input("Custo da ferramenta/inserto (Ct) [$]", value=9.0, step=0.5)
n_t = st.sidebar.number_input("Arestas de corte por inserto (nt)", value=3, step=1)
t_L_min = st.sidebar.number_input("Tempo de troca da ponta (tl) [min]", value=1.0, step=0.1)

# 4. Informações da Máquina e Processo
st.sidebar.subheader("4. Parâmetros da Máquina")
f_rapid = st.sidebar.number_input("Velocidade do avanço rápido [mm/min]", value=6000.0, step=500.0)
t_cs_s = st.sidebar.number_input("Tempo de troca de ferramenta [s]", value=8.0, step=1.0)
t_h_s = st.sidebar.number_input("Tempo de carga/descarga da peça (th) [s]", value=20.0, step=1.0)

# 5. Custos Operacionais
st.sidebar.subheader("5. Custos Operacionais")
C_o_hora = st.sidebar.number_input("Custo operacional da máquina (Co) [$/h]", value=60.0, step=5.0)

# ==========================================
# CÁLCULOS
# ==========================================

# Taxa de custo operacional por minuto ($/min)
C_o = C_o_hora / 60.0

# Custo por aresta de corte ($)
C_te = C_t / n_t

# Velocidade de corte V (m/min)
#V = (np.pi * D * N) / 1000.0
N= 1000 * V / (np.pi * D)

# Tempo de usinagem tm (min)
t_m = (L + Le) / (f * N)

# Vida útil da ferramenta T (min) usando a equação de Taylor: V * T^n = C1
T = (C1 / V) ** (1 / n_taylor) if V > 0 else 0

# Tempos não produtivos em minutos
t_h = t_h_s / 60.0       # Manuseio da peça
t_cs = t_cs_s / 60.0     # Troca da ferramenta entre operações
t_x = (L + Lx) / f_rapid # Avanço/Retorno rápido

# Componentes de custo por unidade ($)
custo_usinagem = C_o * t_m
custo_ferramenta_e_troca = (t_m / T) * (C_o * t_L_min + C_te) if T > 0 else 0
custo_nao_produtivo = C_o * (t_cs + t_h + t_x)

# Custo Total Unitário Cu ($)
C_u = custo_usinagem + custo_ferramenta_e_troca + custo_nao_produtivo

# ==========================================
# EXIBIÇÃO DOS RESULTADOS
# ==========================================

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Parâmetros Calculados")
    st.metric("Velocidade do eixo-árvore (N)", f"{N:.2f} rpm")
    st.metric("Tempo de Usinagem (tm)", f"{t_m:.3f} min ({t_m * 60:.1f} s)")
    st.metric("Vida Útil da Ferramenta (T)", f"{T:.2f} min")
    st.metric("Tempo Rápido (tx)", f"{t_x:.3f} min ({t_x * 60:.1f} s)")
    st.metric("Custo por Aresta (Cte)", f"${C_te:.2f}")

with col2:
    st.subheader("💵 Decomposição dos Custos")
    st.metric("Custo de Usinagem Direto", f"${custo_usinagem:.3f}")
    st.metric("Custo de Ferramenta e Troca", f"${custo_ferramenta_e_troca:.3f}")
    st.metric("Custo Não Produtivo (Setup/Carga)", f"${custo_nao_produtivo:.3f}")

    st.markdown("---")
    st.success(f"### 🎯 Custo Unitário Total (Cu): **${C_u:.2f}**")

# Exibição da Fórmula e Resumo
st.markdown("---")
st.subheader("📝 Equação do Custo Unitário")
st.latex(r"C_u = C_o \cdot t_m + \frac{t_m}{T} (C_o \cdot t_L + C_{te}) + C_o \cdot (t_{cs} + t_h + t_x)")
# 1. Prepara os valores formatados previamente em variáveis simples
val_Co = f"{C_o:.2f}"
val_tm = f"{t_m:.3f}"
val_T = f"{T:.2f}"
val_tl = f"{t_L_min:.1f}"
val_Cte = f"{C_te:.2f}"
val_tcs = f"{t_cs:.3f}"
val_th = f"{t_h:.3f}"
val_tx = f"{t_x:.3f}"
val_Cu = f"{C_u:.2f}"

# 2. Exibe a substituição limpa usando st.latex
st.caption("Substituição com os valores digitados:")

st.latex(
    f"C_u = {val_Co} \\cdot {val_tm} + \\frac{{{val_tm}}}{{{val_T}}} ({val_Co} \\cdot {val_tl} + {val_Cte}) + {val_Co} \\cdot ({val_tcs} + {val_th} + {val_tx}) = \\mathbf{{{val_Cu}}}"
)
