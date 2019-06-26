from functools import wraps

from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from product_api.domain import Product
from product_api.repo import RepoInterface

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


class ProductEntity(Base):
    __tablename__ = f'products'

    product_id = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    def __init__(self, **fields):
        self.product_id = fields['product_id']
        self.title = fields['title']
        self.price = fields['price']
        self.stock = fields['stock']


class ProductTransformer:

    @staticmethod
    def from_domain_to_entity(domain: Product) -> ProductEntity:
        return ProductEntity(
            product_id=domain.product_id,
            title=domain.title,
            price=domain.price,
            stock=domain.stock
        )

    @staticmethod
    def from_entity_to_domain(entity: ProductEntity) -> Product:
        return Product(
            product_id=entity.product_id,
            title=entity.title,
            price=entity.price,
            stock=entity.stock
        )


class ProductDatabaseRepo(RepoInterface):
    def __init__(self):
        self.session = None
        self.engine = create_engine(f'postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE_NAME}')

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()
        self.create_table_if_not_exists()

    @check_session()
    def create_table_if_not_exists(self):
        try:
            if not self.engine.dialect.has_table(self.engine, ProductEntity.__tablename__):
                Base.metadata.create_all(self.engine)
        except SQLAlchemyError:
            pass

    @check_session()
    def save(self, product: Product):
        product_entity = ProductTransformer.from_domain_to_entity(product)
        self.session.add(product_entity)

        return product_entity.product_id

    @check_session()
    def get(self, product_id):
        raise NotImplementedError

    @check_session()
    def list(self):
        items = self.session.query(ProductEntity).all()
        from_entity_to_domain_items_list = []
        for item in items:
            from_entity_to_domain_items_list.append(ProductTransformer.from_entity_to_domain(item))

        return from_entity_to_domain_items_list

    @check_session()
    def delete(self, product_id):
        self.session.query(ProductEntity).filter(ProductEntity.product_id == product_id).delete()

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
