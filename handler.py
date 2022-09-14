import json

from exampleco.models.database import session
from exampleco.models.database.orders import Order, OrderSchema, OrderRequestSchema
from exampleco.models.database.services import ServiceSchema, Service, ServiceRequestSchema


# pylint: disable=unused-argument
def get_all_orders(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """

    orders_schema = OrderSchema(many=True)
    orders = session.query(Order).filter_by(active_status=True).all()
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


# pylint: disable=unused-argument
def get_all_services(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all services pulled from the database.
    """
    services_schema = ServiceSchema(many=True)
    services = session.query(Service).all()
    results = services_schema.dump(services)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response


def add_service(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all services pulled from the database.
    """
    data = ServiceRequestSchema().loads(event["body"])
    service = Service(**data)
    session.add(service)
    session.commit()
    services_schema = ServiceSchema()
    results = services_schema.dump(service)
    response = {"statusCode": 201, "body": json.dumps(results)}

    return response


def delete_order(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """
    order = session.query(Order).get(event["pathParameters"]["id"])

    if order:
        order.active_status = False
        session.add(order)
        session.commit()
        return {"statusCode": 204}

    return {"statusCode": 404}


def update_order(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """

    orders_schema = OrderRequestSchema()
    data = orders_schema.loads(event["body"])
    order = session.query(Order).get(event["pathParameters"]["id"])

    if order.active_status:
        order.description = data["description"]
        db_services = session.query(Service).filter(Service.id.in_(data["services"])).all()
        order.service = db_services
        order.active_status = data.get("active_status", order.active_status)
        session.add(order)
    result = OrderSchema().dump(order)
    session.commit()
    response = {"statusCode": 200, "body": json.dumps(result)}

    return response


def add_order(event, context):
    """
    Example function that demonstrates grabbing list or orders from database

    Returns:
        Returns a list of all orders pulled from the database.
    """

    orders_schema = OrderSchema()
    data = OrderRequestSchema().loads(event["body"])
    service = session.query(Service).filter(Service.id.in_(data["services"])).all()
    order = Order(description=data["description"], active_status=data["active_status"])
    order.service = service
    session.add(order)
    session.commit()
    results = orders_schema.dump(order)

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response
