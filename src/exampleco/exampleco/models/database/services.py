from sqlalchemy import Column, Float, Integer, String, TEXT
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemySchema

from .base import TimeStampedModel


class Service(TimeStampedModel):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    description = Column(TEXT, nullable=True)
    price = Column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"<Service(name='{self.name}', price='{self.price}', created_on='{self.created_on}')>"


class ServiceSchema(SQLAlchemySchema):
    class Meta:
        model = Service
        load_instance = True

    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String()
    price = fields.Float(required=True)
    created_on = fields.DateTime()
    modified_on = fields.DateTime()


class ServiceRequestSchema(Schema):
    description = fields.String(required=True)
    name = fields.String(required=True)
    price = fields.Float(required=True)
