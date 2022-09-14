from sqlalchemy import Column, Table, ForeignKey

from . import Base

OrderItem = Table(
    "order_items",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("service_id", ForeignKey("services.id"), primary_key=True),
)
