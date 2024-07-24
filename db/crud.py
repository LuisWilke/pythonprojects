from .models import users_table
from . import engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def add_user(username, password, cpf):
    with engine.connect() as connection:
        insert_stmt = users_table.insert().values(username=username, password=password, cpf=cpf)
        connection.execute(insert_stmt)

def get_all_users():
    with engine.connect() as connection:
        result = connection.execute(users_table.select())
        return result.fetchall()

def authenticate_user(username, password):
    with engine.connect() as connection:
        query = users_table.select().where(users_table.c.username == username).where(users_table.c.password == password)
        result = connection.execute(query).fetchone()
        return result is not None
