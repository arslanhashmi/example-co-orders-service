from sqlalchemy import Column, Table, ForeignKey

from .base import TimeStampedModel

OrderItem = Table(
    "order_items",
    TimeStampedModel.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("service_id", ForeignKey("services.id"), primary_key=True),
)
