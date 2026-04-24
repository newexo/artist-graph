from sqlalchemy import Boolean, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class PersonRecord(Base):
    __tablename__ = "person"

    tmdb_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    profile_path = Column(String, nullable=True)
    popularity = Column(Float, default=0.0)
    has_full_filmography = Column(Boolean, default=False, nullable=False)

    credits = relationship("CreditRecord", back_populates="person")


class MovieRecord(Base):
    __tablename__ = "movie"

    tmdb_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(Date, nullable=True)
    poster_path = Column(String, nullable=True)
    popularity = Column(Float, default=0.0)
    has_full_cast = Column(Boolean, default=False, nullable=False)

    credits = relationship("CreditRecord", back_populates="movie")


class CreditRecord(Base):
    __tablename__ = "credit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(
        Integer, ForeignKey("person.tmdb_id"), nullable=False, index=True
    )
    movie_id = Column(Integer, ForeignKey("movie.tmdb_id"), nullable=False, index=True)
    character = Column(String, nullable=True)
    credit_order = Column(Integer, nullable=True)

    person = relationship("PersonRecord", back_populates="credits")
    movie = relationship("MovieRecord", back_populates="credits")
