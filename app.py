import streamlit as st
from db.crud import add_user, get_all_users

st.title('Tela de Cadastro')

username = st.text_input('Nome de Usuário')
password = st.text_input('Senha', type='password')
cpf = st.text_input('CPF')

if st.button('Cadastrar'):
    if username and password and cpf:
        try:
            add_user(username, password, cpf)
            st.success('Cadastro realizado com sucesso!')
        except Exception as e:
            st.error(f'Erro ao cadastrar: {e}')
    else:
        st.warning('Por favor, preencha todos os campos.')

# Para visualizar os dados cadastrados (opcional)
if st.checkbox('Mostrar dados cadastrados'):
    users_data = get_all_users()
    st.write(users_data)
