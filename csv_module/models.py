from datetime import datetime

from sqlalchemy import Table, Column, Integer, TIMESTAMP, String, MetaData

metadata = MetaData()

file = Table(
    'file',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(length=32), nullable=False),
    Column('upload_date', TIMESTAMP, default=datetime.utcnow)
)

