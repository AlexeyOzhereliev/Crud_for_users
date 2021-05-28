from datetime import datetime

import sqlalchemy

from database import metadata, engine


users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("hashed_password", sqlalchemy.String),
    sqlalchemy.Column("first_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("last_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column('created_time', sqlalchemy.DateTime, default=datetime.utcnow),
    sqlalchemy.Column('updated_time', sqlalchemy.DateTime, default=datetime.utcnow),
    sqlalchemy.Column("is_active", sqlalchemy.Boolean)
)

metadata.create_all(engine)