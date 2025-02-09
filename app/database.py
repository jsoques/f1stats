from sqlmodel import SQLModel, Session, create_engine

sqlite_file_name = "datastore/f1db.db?mode=ro"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {
    "check_same_thread": False,
    "isolation_level": "IMMEDIATE",
}  # special case for SQLite
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

# !!!!!! Not really needed as the database is read-only
# checkout tips: https://www.powersync.com/blog/sqlite-optimizations-for-ultra-high-performance
# with Session(engine) as session:
#     session.exec(text("PRAGMA journal_mode = WAL"))
#     session.exec(text("PRAGMA synchronous = normal"))
#     session.exec(text("PRAGMA foreign_keys = on"))
#     session.exec(text("PRAGMA journal_size_limit = 6144000"))
#     session.commit()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def close_db():
    engine.dispose()


def get_db():
    db = Session(autoflush=False, bind=engine)
    try:
        yield db
    finally:
        db.close()


def get_session():
    with Session(engine) as session:
        yield session
