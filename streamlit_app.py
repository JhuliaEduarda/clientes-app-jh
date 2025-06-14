import streamlit as st
import sqlite3

##Banco de Dados

def conectar():

    return sqlite3.connect("database.db")

def criar_tabela():
    ##conectando ao Banco de Dados
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clientes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    sexo TEXT,
                    email TEXT
                   )
                   """)
    conexao.commit()
    conexao.close()

def inserir_cliente(nome,sexo,email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
                    INSERT INTO clientes(nome,sexo,email)
                    VALUES (?,?,?)  
                    """, (nome,sexo,email))
    conexao.commit()
    conexao.close()

def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(" SELECT * FROM clientes ")
    clientes = cursor.fetchall()
    conexao.close()

    return clientes

def atualizar_clientes(id,nome,sexo,email):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
                    UPTADE clientes SET nome=?,sexo=?,email=?
                   WHERE id=?
                   """,(nome,sexo,email,id))
    conexao.commit()
    conexao.close()
    
def deletar_clientes(id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(" DELETE FROM clientes WHERE id = ? ",(id,))
    conexao.commit()
    conexao.close()
    

##Front-end
st.title("❐ Sistema de Vendas ")
st.write(
    'Seja Bem vindo!!'
)
#chamou a função criar_tabela()
criar_tabela()

menu = ['Opções:','Cadastrar','Listar / Alterar / Excluir']
escolha = st.sidebar.selectbox("Menu: ",menu)

if escolha == 'Cadastrar':
    ##st.success('Você escolheu a opção cadastrar')

    with st.form(key='form'):
        nome = st.text_input("Nome: ")
        sexo = st.selectbox('Sexo: ',['Masculino','Feminino','Prefiro Não Informar'])
        email = st.text_input("Email: ")
        submit = st.form_submit_button('Cadastrar')
        if submit:
            inserir_cliente(nome,sexo,email)
            st.success(f"Cliente {nome} cadastrado com Sucesso!!")

elif escolha == 'Listar / Alterar / Excluir':
    st.subheader("Clientes Cadastrados")
    ##st.success('Você escolheu a opção Listar')

    clientes = listar_clientes()
    if not clientes:
        st.info("Não existem clientes cadastrados.")
    else:
        for c in clientes:
            with st.expander(f"{c[1]} - {c[2]}"):
                novo_nome = st.text_input(f"Nome - ID {c[0]}",value=c[1],key=f"nome{c[0]}")
                novo_sexo = st.selectbox(f"Sexo",['Masculino','Feminino','Prefiro Não Informar'],index=['Masculino','Feminino','Prefiro Não Informar'].index(c[2]),key=f"sexo{c[0]}")
                novo_email = st.text_input(f"Email",value=c[3],key=f"email{c[0]}")

                col1,col2 = st.columns(2)
                if col1.button("Atualizar", key=f"update{c[0]}"):
                    atualizar_clientes(c[0], novo_nome, novo_sexo, novo_email)
                    st.success("Atualizado com Sucesso.")
                    st.rerun()
                if col2.button("Excluir", key=f"delete{c[0]}"):
                    deletar_clientes(c[0])
                    st.warning("Cliente Excluído.")
                    st.rerun()
