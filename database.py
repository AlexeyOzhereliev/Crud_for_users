import os
import databases
import sqlalchemy
import dotenv

dotenv.load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(
    DATABASE_URL)