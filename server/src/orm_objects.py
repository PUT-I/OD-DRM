from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(length=64), nullable=False, unique=True)
    password = Column(String(length=64), nullable=False)
    authorized = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Person(username='{self.username}', password='{self.password}')>"


def init_db(host: str = "localhost", port: int = 3306) -> None:
    from sqlalchemy import create_engine

    engine = create_engine(f"mysql://root:admin@{host}:{port}/pokevisor", echo=True)
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
