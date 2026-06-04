import streamlit as st
import numpy as np
import pandas as pd
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import funcionesCalculo as ft

# ---------------------------------------------------------------------------
# Configuración de la página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title='Tensiones Terraplén',
    page_icon='🏗️',
    layout='wide',
    initial_sidebar_state='expanded',
)

st.title('🏗️ Análisis Tenso-Deformacional de Terraplén')
st.caption('Basado en la formulación de D.L. Holl — uso académico')

# ---------------------------------------------------------------------------
# SIDEBAR — Datos de entrada
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header('⚙️ Parámetros de entrada')

    # --- Geometría del terraplén ---
    with st.expander('📐 Geometría del terraplén', expanded=True):
        a = st.number_input('Ancho del derrame a (m)', min_value=0.1, value=10.0,
                            step=0.5, format='%.2f',
                            help='Ancho horizontal de cada talud del terraplén')
        b = st.number_input('Semiancho de la coronación b (m)', min_value=0.1, value=15.0,
                            step=0.5, format='%.2f',
                            help='Semiancho de la plataforma superior')
        h = st.number_input('Altura H (m)', min_value=0.1, value=6.0,
                            step=0.5, format='%.2f')
        pe_terraplen = st.number_input('Peso específico del relleno γ (kN/m³)',
                                       min_value=10.0, value=18.0, step=0.5, format='%.2f')
        q = pe_terraplen * h
        st.info(f'Carga aplicada **q = γ·H = {q:.1f} kN/m²**')

    # --- Nivel freático ---
    with st.expander('💧 Nivel freático', expanded=False):
        nivel_freatico = st.number_input('Profundidad del nivel freático (m)',
                                         min_value=0.0, value=5.0, step=0.5, format='%.2f',
                                         help='Medida desde la superficie del terreno natural')

    # --- Malla de cálculo ---
    with st.expander('🔢 Malla de cálculo', expanded=False):
        incrx = st.number_input('Incremento Δx (m)', min_value=0.1, value=1.0,
                                step=0.1, format='%.2f')
        incrz = st.number_input('Incremento Δz (m)', min_value=0.1, value=0.5,
                                step=0.1, format='%.2f')
        ax_banda = st.number_input('Semiancho de la banda de cálculo (m)',
                                   min_value=1.0, value=20.0, step=1.0, format='%.1f',
                                   help='Extensión lateral más allá del pie del terraplén')

    st.markdown('---')

    # --- Botón de cálculo ---
    calcular = st.button('▶️ Calcular', type='primary', use_container_width=True)

# ---------------------------------------------------------------------------
# MAIN — Datos del terreno (tabla editable de capas)
# ---------------------------------------------------------------------------
st.subheader('🌍 Perfil estratigráfico del terreno')

col_info, col_ncapas = st.columns([3, 1])
with col_ncapas:
    n_capas = st.number_input('Número de capas', min_value=1, max_value=20,
                               value=3, step=1)

# Tabla editable de capas
capas_default = {
    'Espesor (m)': [4.0, 6.0, 10.0],
    'γ seco (kN/m³)': [17.0, 18.0, 19.0],
    'γ sat. (kN/m³)': [20.0, 21.0, 22.0],
    'E (kPa)': [15000.0, 25000.0, 40000.0],
    'ν (Poisson)': [0.3, 0.3, 0.25],
    'c (kPa)': [10.0, 15.0, 20.0],
    'φ (°)': [25.0, 28.0, 30.0],
    'Tipo (E=elástico)': ['E', 'E', 'E'],
}

# Ajustar número de filas al número de capas seleccionado
if 'df_capas' not in st.session_state or len(st.session_state.df_capas) != n_capas:
    df_init = pd.DataFrame(capas_default)
    if n_capas <= len(df_init):
        df_init = df_init.iloc[:n_capas].copy()
    else:
        extras = n_capas - len(df_init)
        fila_extra = pd.DataFrame({
            'Espesor (m)': [5.0] * extras,
            'γ seco (kN/m³)': [18.0] * extras,
            'γ sat. (kN/m³)': [21.0] * extras,
            'E (kPa)': [30000.0] * extras,
            'ν (Poisson)': [0.3] * extras,
            'c (kPa)': [10.0] * extras,
            'φ (°)': [28.0] * extras,
            'Tipo (E=elástico)': ['E'] * extras,
        })
        df_init = pd.concat([df_init, fila_extra], ignore_index=True)
    st.session_state.df_capas = df_init

df_capas = st.data_editor(
    st.session_state.df_capas,
    use_container_width=True,
    num_rows='fixed',
    column_config={
        'Espesor (m)': st.column_config.NumberColumn(min_value=0.1, format='%.2f'),
        'γ seco (kN/m³)': st.column_config.NumberColumn(min_value=1.0, format='%.2f'),
        'γ sat. (kN/m³)': st.column_config.NumberColumn(min_value=1.0, format='%.2f'),
        'E (kPa)': st.column_config.NumberColumn(min_value=1.0, format='%.1f'),
        'ν (Poisson)': st.column_config.NumberColumn(min_value=0.0, max_value=0.5, format='%.3f'),
        'c (kPa)': st.column_config.NumberColumn(min_value=0.0, format='%.2f'),
        'φ (°)': st.column_config.NumberColumn(min_value=0.0, max_value=45.0, format='%.1f'),
        'Tipo (E=elástico)': st.column_config.SelectboxColumn(options=['E', 'e']),
    },
    key='editor_capas',
)
st.session_state.df_capas = df_capas

# Croquis del terraplén
with st.expander('📏 Vista previa de la geometría del terraplén', expanded=False):
    fig_croquis = ft.figura_perfil_terraplen(a, b, h)
    st.pyplot(fig_croquis, use_container_width=True)
    plt.close(fig_croquis)

st.markdown('---')

# ---------------------------------------------------------------------------
# CÁLCULO
# ---------------------------------------------------------------------------

def construir_parametros_terreno(df):
    """Convierte el DataFrame de capas en listas para las funciones de cálculo."""
    espesores = [0.0] + list(df['Espesor (m)'].astype(float))
    cotas = [sum(espesores[:i+1]) for i in range(len(espesores))]
    # índice 0 es ficticio (superficie)
    pe_seco = [0.0] + list(df['γ seco (kN/m³)'].astype(float))
    pe_sat = [0.0] + list(df['γ sat. (kN/m³)'].astype(float))
    E = [0.0] + list(df['E (kPa)'].astype(float))
    poisson = [0.0] + list(df['ν (Poisson)'].astype(float))
    cohesion = [0.0] + list(df['c (kPa)'].astype(float))
    fi = [0.0] + list(df['φ (°)'].astype(float))
    tipo_calculo = [0] + list(df['Tipo (E=elástico)'].astype(str))
    return cotas, pe_seco, pe_sat, E, poisson, cohesion, fi, tipo_calculo


def fig_a_bytes(fig):
    """Convierte figura matplotlib a BytesIO PNG."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    buf.seek(0)
    return buf


if calcular:
    # Validaciones básicas
    errores = []
    if df_capas['Espesor (m)'].sum() < incrz:
        errores.append('La profundidad total del perfil es menor que el incremento Δz.')
    if a <= 0 or b <= 0 or h <= 0:
        errores.append('Los parámetros geométricos del terraplén deben ser positivos.')

    if errores:
        for e in errores:
            st.error(e)
        st.stop()

    with st.spinner('Calculando... puede tardar unos segundos según la densidad de la malla.'):
        cotas, pe_seco, pe_sat, E, poisson, cohesion, fi, tipo_calculo = \
            construir_parametros_terreno(df_capas)

        resultados = ft.calcular_todo(
            a=a, b=b, h=h, q=q,
            ax=ax_banda, incrx=incrx, incrz=incrz,
            cotas=cotas,
            nivel_freatico=nivel_freatico,
            pe_seco=pe_seco,
            pe_saturado=pe_sat,
            E=E, poisson=poisson,
            cohesion=cohesion, fi=fi,
            tipo_calculo=tipo_calculo,
        )

    st.session_state['resultados'] = resultados
    st.session_state['calculado'] = True
    st.success(f'✅ Cálculo completado — Asiento máximo: **{resultados["asiento_max"]*100:.2f} cm**')

# ---------------------------------------------------------------------------
# RESULTADOS — Tabs
# ---------------------------------------------------------------------------

if st.session_state.get('calculado'):
    res = st.session_state['resultados']
    xcoord = res['xcoord']
    zcoord = res['zcoord']

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        '📊 Tensiones Δσz',
        '📊 Tensiones Δσx',
        '📊 Tensiones Δτxz',
        '📊 Tensiones naturales',
        '📉 Asientos',
        '📥 Descargar resultados',
    ])

    # ---- Tab 1: Δσz ----
    with tab1:
        st.subheader('Incremento de tensión vertical Δσz [kN/m²]')
        c1, c2 = st.columns(2)
        with c1:
            fig = ft.figura_tensiones(xcoord, zcoord, res['tension_z'],
                                      'Δσz', 'contorno', a, b, h)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with c2:
            fig = ft.figura_tensiones(xcoord, zcoord, res['tension_z'],
                                      'Δσz', 'isolinea', a, b, h)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown('**Valores en el eje (x = 0) por profundidad:**')
        idx_eje = np.argmin(np.abs(xcoord))
        df_sz = pd.DataFrame({
            'Profundidad z (m)': np.round(zcoord, 3),
            'Δσz (kN/m²)': np.round(res['tension_z'][:, idx_eje], 4),
        })
        st.dataframe(df_sz, use_container_width=True, hide_index=True)

    # ---- Tab 2: Δσx ----
    with tab2:
        st.subheader('Incremento de tensión horizontal Δσx [kN/m²]')
        c1, c2 = st.columns(2)
        with c1:
            fig = ft.figura_tensiones(xcoord, zcoord, res['tension_x'],
                                      'Δσx', 'contorno', a, b, h)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with c2:
            fig = ft.figura_tensiones(xcoord, zcoord, res['tension_x'],
                                      'Δσx', 'isolinea', a, b, h)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown('**Valores en el eje (x = 0) por profundidad:**')
        idx_eje = np.argmin(np.abs(xcoord))
        df_sx = pd.DataFrame({
            'Profundidad z (m)': np.round(zcoord, 3),
            'Δσx (kN/m²)': np.round(res['tension_x'][:, idx_eje], 4),
        })
        st.dataframe(df_sx, use_container_width=True, hide_index=True)

    # ---- Tab 3: Δτxz ----
    with tab3:
        st.subheader('Incremento de tensión tangencial Δτxz [kN/m²]')
        c1, c2 = st.columns(2)
        with c1:
            fig = ft.figura_tensiones(xcoord, zcoord, res['tension_xz'],
                                      'Δτxz', 'contorno', a, b, h)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with c2:
            fig = ft.figura_tensiones(xcoord, zcoord, res['tension_xz'],
                                      'Δτxz', 'isolinea', a, b, h)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        st.markdown('**Valores en el eje (x = 0) por profundidad:**')
        idx_eje = np.argmin(np.abs(xcoord))
        df_txz = pd.DataFrame({
            'Profundidad z (m)': np.round(zcoord, 3),
            'Δτxz (kN/m²)': np.round(res['tension_xz'][:, idx_eje], 4),
        })
        st.dataframe(df_txz, use_container_width=True, hide_index=True)

    # ---- Tab 4: Tensiones naturales ----
    with tab4:
        st.subheader('Tensiones naturales del terreno')
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('**Tensión total vertical σz,0**')
            fig = ft.figura_tensiones(xcoord, zcoord, res['tension_z_terreno'],
                                      'σz total', 'contorno', a, b, h)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        with c2:
            st.markdown('**Tensión efectiva vertical σ\'z,0**')
            fig = ft.figura_tensiones(xcoord, zcoord, res['tension_z_efectiva'],
                                      'σz efectiva', 'contorno', a, b, h)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)

        idx_eje = np.argmin(np.abs(xcoord))
        df_nat = pd.DataFrame({
            'Profundidad z (m)': np.round(zcoord, 3),
            'σz total (kN/m²)': np.round(res['tension_z_terreno'][:, idx_eje], 4),
            'σz efectiva (kN/m²)': np.round(res['tension_z_efectiva'][:, idx_eje], 4),
        })
        st.dataframe(df_nat, use_container_width=True, hide_index=True)

    # ---- Tab 5: Asientos ----
    with tab5:
        st.subheader('Perfil de asientos en superficie')

        fig_as = ft.figura_asientos(xcoord, res['asiento'], b, a, h)
        st.pyplot(fig_as, use_container_width=True)
        plt.close(fig_as)

        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric('Asiento máximo', f'{res["asiento_max"]*100:.2f} cm')
        col_m2.metric('Asiento mín. (borde)', f'{float(np.max(res["asiento"]))*100:.2f} cm')
        col_m3.metric('Profundidad total analizada', f'{zcoord[-1]:.1f} m')

        df_as = pd.DataFrame({
            'x (m)': np.round(xcoord, 3),
            'Asiento (m)': np.round(res['asiento'], 6),
            'Asiento (cm)': np.round(np.array(res['asiento']) * 100, 4),
        })
        st.dataframe(df_as, use_container_width=True, hide_index=True)

    # ---- Tab 6: Descargar ----
    with tab6:
        st.subheader('📥 Descarga de resultados')

        params_tp = {
            'a': a, 'b': b, 'h': h, 'pe': pe_terraplen, 'q': q,
            'nivel_freatico': nivel_freatico,
            'incrx': incrx, 'incrz': incrz, 'ax': ax_banda,
        }
        capas_data = []
        for _, row in df_capas.iterrows():
            capas_data.append({
                'espesor': row['Espesor (m)'],
                'pe_seco': row['γ seco (kN/m³)'],
                'pe_sat': row['γ sat. (kN/m³)'],
                'E': row['E (kPa)'],
                'poisson': row['ν (Poisson)'],
                'cohesion': row['c (kPa)'],
                'fi': row['φ (°)'],
                'tipo_calculo': row['Tipo (E=elástico)'],
            })

        col_d1, col_d2 = st.columns(2)

        # Excel
        with col_d1:
            st.markdown('### 📊 Excel completo')
            st.markdown('6 hojas: datos de entrada, 5 matrices de tensiones y asientos.')
            with st.spinner('Generando Excel...'):
                excel_bytes = ft.generar_excel_resultados(res, params_tp, capas_data)
            st.download_button(
                label='⬇️ Descargar Excel',
                data=excel_bytes,
                file_name='resultados_terraplen.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True,
            )

        # Word
        with col_d2:
            st.markdown('### 📄 Informe Word')
            st.markdown('Portada, datos, figuras y conclusiones automáticas.')
            with st.spinner('Generando informe Word...'):
                # Generar figuras para el Word
                figuras_bytes = {}

                fig_tmp = ft.figura_tensiones(xcoord, zcoord, res['tension_z'],
                                              'Δσz', 'contorno', a, b, h)
                figuras_bytes['sz_contorno'] = fig_a_bytes(fig_tmp)
                plt.close(fig_tmp)

                fig_tmp = ft.figura_tensiones(xcoord, zcoord, res['tension_z'],
                                              'Δσz', 'isolinea', a, b, h)
                figuras_bytes['sz_isolinea'] = fig_a_bytes(fig_tmp)
                plt.close(fig_tmp)

                fig_tmp = ft.figura_tensiones(xcoord, zcoord, res['tension_x'],
                                              'Δσx', 'contorno', a, b, h)
                figuras_bytes['sx_contorno'] = fig_a_bytes(fig_tmp)
                plt.close(fig_tmp)

                fig_tmp = ft.figura_tensiones(xcoord, zcoord, res['tension_xz'],
                                              'Δτxz', 'contorno', a, b, h)
                figuras_bytes['txz_contorno'] = fig_a_bytes(fig_tmp)
                plt.close(fig_tmp)

                fig_tmp = ft.figura_asientos(xcoord, res['asiento'], b, a, h)
                figuras_bytes['asientos'] = fig_a_bytes(fig_tmp)
                plt.close(fig_tmp)

                word_bytes = ft.generar_word_informe(res, params_tp, capas_data, figuras_bytes)

            st.download_button(
                label='⬇️ Descargar Informe Word',
                data=word_bytes,
                file_name='informe_terraplen.docx',
                mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                use_container_width=True,
            )

else:
    st.info('👆 Introduce los parámetros en el panel lateral y pulsa **▶️ Calcular** para ver los resultados.')
