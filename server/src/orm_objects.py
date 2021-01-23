from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    authorized = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Person(username='{self.username}', password='{self.password}')>"


def _main():
    from sqlalchemy import create_engine

    engine = create_engine("sqlite:///database.sqlite", echo=True)

    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    _main()
