import json

from exampleco.models.database import session
from exampleco.models.database.orders import Order, OrderSchema
from exampleco.models.database.services import ServiceSchema, Service


# pylint: disable=unused-argument
def get_all_orders(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """

    orders_schema = OrderSchema(many=True)
    orders = session.query(Order).all()
    results = orders_schema.dump(orders)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response


# pylint: disable=unused-argument
def get_service(event, context):
    """
    Retrieves a service given its ID.

    Returns:
        Returns a service given a service ID from the database.
    """
    services_schema = ServiceSchema()
    service = session.query(Service).get(event["pathParameters"]["id"])
    results = services_schema.dump(service)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response
