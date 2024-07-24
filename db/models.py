from sqlalchemy import Table, Column, Integer, String
from . import metadata, engine

users_table = Table('users', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('username', String, unique=True),
                    Column('password', String),
                    Column('cpf', String, unique=True)
                    )

# Criação da tabela no banco de dados
metadata.create_all(bind=engine)
