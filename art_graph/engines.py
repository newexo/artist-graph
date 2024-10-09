import sqlalchemy


def get_engine(absolute_path) -> sqlalchemy.Engine:
    return sqlalchemy.create_engine(f"sqlite:////{absolute_path}")
