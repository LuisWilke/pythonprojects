from sqlalchemy import create_engine, MetaData

DATABASE_URL = "sqlite:///login_data.db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()
