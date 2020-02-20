from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .model import Base

Session = sessionmaker()


def use_database_file(database):
    # Set up database file or use in-memory db
    if database == ":memory:":
        print(f"Using a transient in-memory database...")
    else:
        print(f"Using database at {database}...")         
    db_path = f"sqlite:///{database}"
    print("Binding the database session...")
    engine = create_engine(db_path)
    Session.configure(bind=engine)


def create_schema(args):
    use_database_file(args.database)
    session = Session()
    engine = session.get_bind()
    print("Creating the schema using the declarative base...")
    Base.metadata.create_all(engine)
