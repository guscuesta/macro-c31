# Streamlit: Simulador de consumo estilo Blanchard
# C = c0 + c1·(Y - T)  con eje X = YD (renta disponible) y recta de 45°
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Simulador Consumo (Blanchard)", layout="wide")

st.title("Función de consumo: C = c₀ + c₁·(Y − T)")
# ----- Panel lateral (parámetros) -----
with st.sidebar:
    st.header("Parámetros")
    c0 = st.number_input("c₀ (consumo autónomo)", value=200.0, step=10.0, format="%.2f")
    c1 = st.slider("c₁ (propensión marginal a consumir)", min_value=0.0, max_value=1.0, value=0.75, step=0.01)
    T  = st.number_input("T (impuestos)", value=200.0, step=10.0, format="%.2f")
    Ymin = st.number_input("Ymin (renta total)", value=0.0, step=50.0, format="%.2f")
    Ymax = st.number_input("Ymax (renta total)", value=2000.0, step=50.0, format="%.2f")
    step = st.number_input("ΔY (paso)", value=100.0, min_value=1.0, step=1.0, format="%.0f")

    st.markdown("---")
    st.subheader("Ejes fijos (gráfico)")
    X_MIN = st.number_input("X_MIN (YD mínimo)", value=0.0, step=50.0, format="%.0f")
    X_MAX = st.number_input("X_MAX (YD máximo)", value=2000.0, step=50.0, format="%.0f")
    Y_MIN = st.number_input("Y_MIN (C mínimo)", value=0.0, step=50.0, format="%.0f")
    Y_MAX = st.number_input("Y_MAX (C máximo)", value=2000.0, step=50.0, format="%.0f")

# ----- Datos -----
Ys = np.arange(Ymin, Ymax + 1e-9, step, dtype=float)   # renta total
YD = Ys - T                                           # renta disponible (X)
C  = c0 + c1 * YD                                     # consumo (Y)
df = pd.DataFrame({"Y": Ys, "YD": YD, "C": C})

# ----- Layout -----
col_plot, col_info = st.columns([2, 1])

with col_plot:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    # Curva de consumo vs YD (NO fijar colores explícitos)
    ax.plot(df["YD"], df["C"], label="C = c₀ + c₁·(Y − T)", linewidth=2)
       # Ejes fijos
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(Y_MIN, Y_MAX)
    ax.set_xlabel("Renta disponible (Y − T)")
    ax.set_ylabel("Consumo (C)")
    ax.legend()
    st.pyplot(fig)

with col_info:
    st.subheader("Parámetros actuales")
    st.write(f"**c₀** = {c0:,.2f} · **c₁** = {c1:,.2f} · **T** = {T:,.2f}")
    
    # Descarga CSV
    st.subheader("Descargar datos")
    st.download_button(
        "Descargar CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="tabla_consumo.csv",
        mime="text/csv",
    )

st.subheader("Tabla (primeras 15 filas)")
st.dataframe(df.head(15), use_container_width=True)


