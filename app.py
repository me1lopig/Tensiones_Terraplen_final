
import streamlit as st

# Entrada de datos del terraplen

st.write("## Datos geometricos del terraplén")

derrame = st.number_input("Derrame (m)",step=1.0, value=10.0, format="%.2f")
semiancho = st.number_input("Semiancho(m)",step=1.0, value=15.0, format="%.2f")
altura = st.number_input("Altura (m)",step=1.0, value=6.0, format="%.2f")


# colocar aqui el codigo para hacer el dibujo del terraplén


# Materiales del terraplén
st.write("## Datos del material  del terraplén")
pesoEspecifico = st.number_input("peso específico kN/m3",step=1.0, value=18.00, format="%.2f")


# Datos de la malla de cálculo
st.write("## Datos de la malla de cálculo")

incrx = st.number_input("Incremento malla x",step=0.10, min_value=0.10,value=0.10, format="%.2f")
incrz = st.number_input("Incremento malla z",step=0.10, min_value=0.10,value=0.1, format="%.2f")


