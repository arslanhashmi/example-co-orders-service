import json
from datetime import datetime

from dateutil.relativedelta import relativedelta

from exampleco.models.database import session
from exampleco.models.database.orders import Order, OrderSchema, OrderRequestSchema
from exampleco.models.database.services import ServiceSchema, Service, ServiceRequestSchema


def span_mapper(span):
    now = datetime.now()
    if span == 'THIS_YEAR':
        span_time = now - relativedelta(day=1, month=1)   # Keeping same year and setting to 1st Jan day start
    elif span == 'THIS_WEEK':
        span_time = now - relativedelta(days=now.weekday())
    else:
        span_time = now - relativedelta(day=1)
    return span_time - relativedelta(second=0, minute=0, hour=0)


# pylint: disable=unused-argument
def get_all_orders(event, context):
    """
    List or orders from database

    Returns:
        Returns a list of all orders (that aren't deleted) pulled from the database.
    """
    
    orders_schema = OrderSchema(many=True)
    orders = session.query(Order).filter_by(is_deleted=False)

    if query_params := event.get("queryStringParameters"):
        if span := query_params.get("span", None):
            orders = orders.filter(Order.created_on >= span_mapper(span))

    results = orders_schema.dump(orders.all())

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
    List all services from database

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
    Adds new service

    Returns:
        Returns newly added service to the database.
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
    Deletes order

    Returns:
        Returns 200 status code on setting delete status on order valid order
    """
    order = session.query(Order).get(event["pathParameters"]["id"])

    if order:
        order.active_status = False
        session.add(order)
        session.commit()
        return {"statusCode": 200}

    return {"statusCode": 404}


def update_order(event, context):
    """
    Updates order

    Returns:
        Returns updated order
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
    Adds new order

    Returns:
        Returns newly added order to the database
    """

    orders_schema = OrderSchema()
    data = OrderRequestSchema().loads(event["body"])
    service = session.query(Service).filter(Service.id.in_(data["services"])).all()
    order = Order(description=data["description"])
    order.service = service
    session.add(order)
    session.commit()
    results = orders_schema.dump(order)
    from pdb import set_trace; set_trace()

    response = {"statusCode": 200, "body": json.dumps(results)}

    return response
