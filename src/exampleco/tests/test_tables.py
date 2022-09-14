import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from exampleco.models.database.orders import Order
from exampleco.models.database.services import Service
from exampleco.models.database import Base


@pytest.fixture(scope="session")
def connection():
    engine = create_engine(
        "mysql+pymysql://{}:{}@{}/{}".format("admin", "password", "localhost", "db")
    )
    return engine.connect()


def seed_database(session):
    # cleanup any existing records
    session.query(Service).delete()
    session.query(Order).delete()
    session.commit()

    services = [
        {
            "id": 1,
            "name": "Service 1",
            "description": "Service description 1",
            "price": 33.5
        },
        {
            "id": 2,
            "name": "Service 2",
            "description": "Service description 2",
            "price": 50.5
        },
    ]
    for service in services:
        service = Service(**service)
        session.add(service)
    session.commit()

    orders = [
        {
            "id": 1,
            "description": "Order 1",
            "is_deleted": True,
            "service": [session.query(Service).get(1)]
        },
        {
            "id": 2,
            "description": "Order 2",
            "is_deleted": False,
            "service": [session.query(Service).get(2)]
        },
        {
            "id": 3,
            "description": "Order 3",
            "is_deleted": False,
            "service": [session.query(Service).get(2)]
        },
    ]

    for order in orders:
        order = Order(**order)
        session.add(order)
    session.commit()


@pytest.fixture(scope="session")
def setup_database(connection):
    Base.metadata.bind = connection
    Base.metadata.create_all()

    yield

    Base.metadata.drop_all()


@pytest.fixture
def db_session(setup_database, connection):
    transaction = connection.begin()
    session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    seed_database(session)
    yield session
    transaction.rollback()


@pytest.mark.parametrize(
    "order_id,service_id,order_description,service_description,is_order_deleted",
    [
        (1, 1, "Order 1", "Service description 1", True),
        (2, 2, "Order 2", "Service description 2", False),
        (3, 2, "Order 3", "Service description 2", False),
    ]
)
def test_orders_and_services_retrieval(db_session, order_id, service_id,
                             order_description, service_description, is_order_deleted):
    order = db_session.query(Order).get(order_id)
    assert order.description == order_description
    assert order.service[0].id == service_id
    assert order.is_deleted == is_order_deleted
    assert order.service[0].description == service_description


def test_order_created(db_session):
    order_params = {
        "id": 4,
        "description": "Order 4",
        "is_deleted": True,
        "service": [db_session.query(Service).get(1)]
    }
    db_session.add(Order(**order_params))
    db_session.commit()
    order = db_session.query(Order).get(4)
    assert order.description == order_params["description"]
    assert order.is_deleted == order_params["is_deleted"]
    assert order.service[0].description == order_params["service"][0].description


def test_order_updated(db_session):
    order = db_session.query(Order).get(1)
    order.description = "Order 4"
    order.is_deleted = False
    order.service = [db_session.query(Service).get(2)]
    db_session.commit()
    updated_order = db_session.query(Order).get(1)
    assert updated_order.description == order.description
    assert updated_order.is_deleted == order.is_deleted
    assert updated_order.service[0].description == order.service[0].description


def test_service_created(db_session):
    service_params ={
        "id": 3,
        "name": "Service 3",
        "description": "Service description 3",
        "price": 1000
    }
    db_session.add(Service(**service_params))
    db_session.commit()
    service = db_session.query(Service).get(3)
    assert service.name == service_params["name"]
    assert service.description == service_params["description"]
    assert service.price == service_params["price"]


def test_service_updated(db_session):
    service = db_session.query(Service).get(1)
    service.description = "Service description 3"
    service.price = 1000
    db_session.commit()
    updated_service = db_session.query(Service).get(1)
    assert updated_service.name == service.name
    assert updated_service.description == service.description
    assert updated_service.price == service.price
