import streamlit as st
import fdb
import pandas as pd

def get_data_from_firebird(dsn, user, password, query):
    try:
        con = fdb.connect(
            dsn=dsn,
            user=user,
            password=password
        )
        
        cur = con.cursor()
        cur.execute(query)
        
        rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description]
        
        con.close()
        
        return pd.DataFrame(rows, columns=col_names)
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# Interface Streamlit
st.title('Dados do Banco de Dados Firebird')

dsn = st.text_input('DSN', 'c:/ecosis/dados/ecodados.eco')
user = st.text_input('Usuário', 'sysdba')
password = st.text_input('Senha', 'masterkey', type='password')
query = st.text_area('Query SQL', 'SELECT * FROM trecclientegeral')

if st.button('Carregar Dados'):
    with st.spinner('Carregando dados...'):
        data = get_data_from_firebird(dsn, user, password, query)
        if not data.empty:
            st.write(data)
        else:
            st.write("Nenhum dado encontrado.")
