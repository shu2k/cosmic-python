from sqlalchemy import Column, ForeignKey, Integer, String, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, relationship

import model

metadata = MetaData()

order_lines = Table(  # (2)
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
)


def start_mappers():
    lines_mapper = mapper(model.OrderLine, order_lines)
