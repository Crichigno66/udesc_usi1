import streamlit as st
import numpy as np

def calcular_desgaste_vb(vc, f, ap, t):
    """
    Calcula a marca de desgaste VB (mm) com ruído aleatório de ±10%.
    vc: Velocidade de corte (m/min)
    f: Avanço (mm/rot)
    ap: Profundidade de corte (mm)
    t: Tempo de usinagem (min)
    """
    K = 1.185e-6
    x, y, z = 2.128, 0.724, 0.388
    
    # Cálculo teórico base
    vb_teorico = K * (vc ** x) * (f ** y) * (ap ** z) * t
    
    # Aplicação do ruído aleatório entre -10% (0.90) e +10% (1.10)
    fator_ruido = np.random.uniform(0.90, 1.10)
    
    return vb_teorico * fator_ruido

# --- Interface Streamlit ---
st.title("Simulador de Desgaste da Ferramenta (VB)")

col1, col2 = st.columns(2)

with col1:
    vc = st.number_input(
        "Velocidade de Corte - v_c (m/min)",
        min_value=1.0,
        max_value=500.0,
        value=120.0,
        step=5.0,
        format="%.1f"
    )
    f = st.number_input(
        "Avanço - f (mm/rot)",
        min_value=0.01,
        max_value=2.00,
        value=0.20,
        step=0.01,
        format="%.2f"
    )

with col2:
    ap = st.number_input(
        "Profundidade de Corte - a_p (mm)",
        min_value=0.1,
        max_value=10.0,
        value=1.5,
        step=0.1,
        format="%.1f"
    )
    t = st.number_input(
        "Tempo de Usinagem - t (min)",
        min_value=0.1,
        max_value=180.0,
        value=10.0,
        step=1.0,
        format="%.1f"
    )

# Cálculo do desgaste simulado com ruído
vb_calculado = calcular_desgaste_vb(vc, f, ap, t)

st.divider()

# Apresentação do resultado único
st.metric(label="Desgaste Medido (VB)", value=f"{vb_calculado:.2f} mm")

# Botão para simular repetibilidade das medições
st.button("🔄 Realizar Nova Medição")

# Aviso pedagógico de fim de vida da ferramenta
if vb_calculado >= 0.3:
    st.warning("⚠️ Critério de fim de vida da ferramenta atingido (VB >= 0.3 mm).")
