from functools import wraps

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import ARRAY

from order_api.domain import Order
from order_api.repo import RepoInterface

HOSTNAME = 'myworkshopserver.postgres.database.azure.com'
USERNAME = 'admin_user@myworkshopserver'
PASSWORD = '8SW[@uEyAkx8!A{N'
PORT = 5432
DATABASE_NAME = 'postgres'

Base = declarative_base()


def check_session():
    """
    Decorator function to check if the session has been initialized

    :return: callable
    :raises Exception
    """

    def check_session_wrapper(callable_func):
        @wraps(callable_func)
        def decor_inner(instance, *args, **kwargs):
            if not instance.session:
                raise AttributeError('No session. Please use context manager.')

            return callable_func(instance, *args, **kwargs)

        return decor_inner

    return check_session_wrapper


class OrderEntity(Base):
    __tablename__ = f'orders'

    order_id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, nullable=False)
    status = Column(String, nullable=False)
    items = Column(ARRAY(Integer), nullable=False, default=0)

    def __init__(self, **fields):
        self.order_id = fields['order_id']
        self.user_id = fields['user_id']
        self.status = fields['status']
        self.items = fields['items']


class OrderTransformer:

    @staticmethod
    def from_domain_to_entity(domain: Order) -> OrderEntity:
        return OrderEntity(
            order_id=domain.order_id,
            user_id=domain.user_id,
            status=domain.status,
            items=domain.items,
        )

    @staticmethod
    def from_entity_to_domain(entity: OrderEntity) -> Order:
        return Order(
            order_id=entity.order_id,
            user_id=entity.user_id,
            status=entity.status,
            items=entity.items,
        )


class OrderDatabaseRepo(RepoInterface):
    def __init__(self):
        self.session = None
        self.engine = create_engine(f'postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE_NAME}')

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()
        self.create_table_if_not_exists()

    @check_session()
    def create_table_if_not_exists(self):
        try:
            if not self.engine.dialect.has_table(self.engine, OrderEntity.__tablename__):
                Base.metadata.create_all(self.engine)
        except SQLAlchemyError:
            pass

    @check_session()
    def save(self, order: Order):
        order_entity = OrderTransformer.from_domain_to_entity(order)
        self.session.add(order_entity)

        return order_entity.order_id

    @check_session()
    def get(self, order_id):
        raise NotImplementedError

    @check_session()
    def list(self):
        items = self.session.query(OrderEntity).all()
        from_entity_to_domain_items_list = []
        for item in items:
            from_entity_to_domain_items_list.append(OrderTransformer.from_entity_to_domain(item))

        return from_entity_to_domain_items_list

    @check_session()
    def delete(self, order_id):
        self.session.query(OrderEntity).filter(OrderEntity.order_id == order_id).delete()

    def __exit__(self, exc_type, exc_value, traceback):

        if exc_type:
            self.session.rollback()
            self.session.close()
            return False
        else:
            try:
                self.session.commit()
            except Exception as err:
                self.session.rollback()
                self.session.close()

                raise err

        self.session.close()
