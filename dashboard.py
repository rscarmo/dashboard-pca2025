import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Dashboard PCA 2025")

# Carrega os dados
df = pd.read_csv("pca_2025 07_02_25.csv", encoding='iso8859-1', delimiter=';')

st.title("Dashboard PCA 2025")

# Renomeia colunas
df = df.rename(columns={
    'Data estimada para o início do processo de contratação': 'Início Estimado',
    'Data estimada para a conclusão do processo de contratação': 'Conclusão Estimada'
})

# Colunas a exibir
colunas_selecionadas = [
    'Nº DFD', 'Nº do Item no DFD', 'Área requisitante', 'Nome Classe/Grupo', 'Início Estimado', 'Conclusão Estimada'
]

# Valores únicos
todos_dfd = sorted(df['Nº DFD'].dropna().unique())
todas_areas = sorted(df['Área requisitante'].dropna().unique())
todos_grupos = sorted(df['Nome Classe/Grupo'].dropna().unique())

# Layout com 3 colunas lado a lado
col0, col1, col2 = st.columns(3)

# SelectBox 0 - Nº DFD
dfd_selecionado = col0.selectbox("Nº DFD", options=["Todos"] + todos_dfd)

# Se um DFD for escolhido, força os outros filtros para 'Todos'
if dfd_selecionado != "Todos":
    filtro_df = df[df['Nº DFD'] == dfd_selecionado]
    area_selecionada = "Todas"
    grupo_selecionado = "Todos"
else:
    # SelectBox 1 - Área Requisitante
    area_selecionada = col1.selectbox("Área Requisitante", options=["Todas"] + todas_areas)

    # Filtra grupos com base na área (se selecionada)
    if area_selecionada != "Todas":
        grupos_filtrados = sorted(df[df['Área requisitante'] == area_selecionada]['Nome Classe/Grupo'].dropna().unique())
    else:
        grupos_filtrados = todos_grupos

    # SelectBox 2 - Nome Classe/Grupo
    grupo_selecionado = col2.selectbox("Nome Classe/Grupo", options=["Todos"] + grupos_filtrados)

    # Aplica filtros combinados
    filtro_df = df.copy()
    if area_selecionada != "Todas":
        filtro_df = filtro_df[filtro_df['Área requisitante'] == area_selecionada]
    if grupo_selecionado != "Todos":
        filtro_df = filtro_df[filtro_df['Nome Classe/Grupo'] == grupo_selecionado]

# Exibe o DataFrame resultante
st.dataframe(filtro_df[colunas_selecionadas], use_container_width=True, hide_index=True)
