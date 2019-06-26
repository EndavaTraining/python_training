from functools import wraps

from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from user_api.domain import User

from user_api.repo import RepoInterface

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


class UserEntity(Base):
    __tablename__ = f'users'

    user_id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    def __init__(self, **fields):
        self.user_id = fields['user_id']
        self.name = fields['name']


class UserTransformer:

    @staticmethod
    def from_domain_to_entity(domain: User) -> UserEntity:
        return UserEntity(
            user_id=domain.user_id,
            name=domain.name
        )

    @staticmethod
    def from_entity_to_domain(entity: UserEntity) -> User:
        return User(
            user_id=entity.user_id,
            name=entity.name,
        )


class UserDatabaseRepo(RepoInterface):
    def __init__(self):
        self.session = None
        self.engine = create_engine(f'postgresql://{USERNAME}:{PASSWORD}@{HOSTNAME}/{DATABASE_NAME}')

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()
        self.create_table_if_not_exists()

    @check_session()
    def create_table_if_not_exists(self):
        try:
            if not self.engine.dialect.has_table(self.engine, UserEntity.__tablename__):
                Base.metadata.create_all(self.engine)
        except SQLAlchemyError:
            pass

    @check_session()
    def save(self, user: User):
        user_entity = UserTransformer.from_domain_to_entity(user)
        self.session.add(user_entity)

        return user_entity.user_id

    @check_session()
    def get(self, user_id):
        raise NotImplementedError

    @check_session()
    def list(self):
        items = self.session.query(UserEntity).all()
        from_entity_to_domain_items_list = []
        for item in items:
            from_entity_to_domain_items_list.append(UserTransformer.from_entity_to_domain(item))

        return from_entity_to_domain_items_list

    @check_session()
    def delete(self, user_id):
        self.session.query(UserEntity).filter(UserEntity.user_id == user_id).delete()

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
