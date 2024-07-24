import streamlit as st
from db.crud import add_user, get_all_users, authenticate_user

# Configurações iniciais
if 'page' not in st.session_state:
    st.session_state.page = 'signup'

def show_signup_page():
    st.title('Tela de Cadastro')
    
    username = st.text_input('Nome de Usuário')
    password = st.text_input('Senha', type='password')
    cpf = st.text_input('CPF')
    
    if st.button('Cadastrar'):
        if username and password and cpf:
            try:
                add_user(username, password, cpf)
                st.success('Cadastro realizado com sucesso!')
                st.session_state.page = 'login'
                st.experimental_rerun()
            except Exception as e:
                st.error(f'Erro ao cadastrar: {e}')
        else:
            st.warning('Por favor, preencha todos os campos.')

def show_login_page():
    st.title('Tela de Login')
    
    username = st.text_input('Nome de Usuário')
    password = st.text_input('Senha', type='password')
    
    if st.button('Login'):
        if authenticate_user(username, password):
            st.success('Login realizado com sucesso!')
            # Redirecionar para outra página após login (ex: página principal)
            st.write('Bem-vindo ao sistema!')
        else:
            st.error('Nome de usuário ou senha incorretos.')

# Navegação entre páginas
if st.session_state.page == 'signup':
    show_signup_page()
elif st.session_state.page == 'login':
    show_login_page()
