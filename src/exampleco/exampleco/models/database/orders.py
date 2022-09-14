from sqlalchemy import Column, Integer, text, TEXT, TIMESTAMP, Boolean
from sqlalchemy.orm import relationship
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemySchema

from .base import TimeStampedModel
from .order_items import OrderItem
from .services import ServiceSchema


class Order(TimeStampedModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    description = Column(TEXT, nullable=True)
    service = relationship("Service", secondary=OrderItem)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    is_deleted = Column(Boolean, nullable=False, server_default=text("False"))
    modified_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP")
    )

    def __repr__(self) -> str:
        return f"<Order(description='{self.description}', created_on='{self.created_on}')>"


class OrderSchema(SQLAlchemySchema):
    class Meta:
        model = Order
        load_instance = True

    id = fields.Integer()
    description = fields.String(required=True)
    is_deleted = fields.Boolean()
    created_on = fields.DateTime()
    modified_on = fields.DateTime()
    service = fields.Nested(ServiceSchema, many=True)


class OrderRequestSchema(Schema):
    description = fields.String(required=True)
    services = fields.List(fields.Integer, required=True)
