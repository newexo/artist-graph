from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class NameBasics(Base):
    __tablename__ = "name_basics"

    nconst = Column(Integer, primary_key=True)
    knownForTitles = Column(Text)
    primaryName = Column(Text)
    primaryProfession = Column(Text)
    deathYear = Column(Integer)
    birthYear = Column(Integer)

    title_principals = relationship("TitlePrincipals", back_populates="name_basics")


class TitleBasics(Base):
    __tablename__ = "title_basics"

    tconst = Column(Integer, primary_key=True)
    primaryTitle = Column(Text)
    originalTitle = Column(Text)
    titleType = Column(String(16))
    isAdult = Column(Boolean)
    startYear = Column(Integer)
    endYear = Column(Integer)
    runtimeMinutes = Column(Integer)
    genres = Column(Text)

    title_principals = relationship("TitlePrincipals", back_populates="title_basics")
    title_akas = relationship("TitleAkas", back_populates="title_basics")
    title_crew = relationship("TitleCrew", back_populates="title_basics")
    title_episode = relationship("TitleEpisode", back_populates="title_basics")
    title_ratings = relationship("TitleRatings", back_populates="title_basics")


class TitlePrincipals(Base):
    __tablename__ = "title_principals"

    id = Column(Integer, primary_key=True, autoincrement=True)

    tconst = Column(Integer, ForeignKey("title_basics.tconst"))
    nconst = Column(Integer, ForeignKey("name_basics.nconst"))

    ordering = Column(Integer)
    job = Column(String(1024))
    category = Column(String(64))
    characters = Column(String(1024))

    title_basics = relationship("TitleBasics", back_populates="title_principals")
    name_basics = relationship("NameBasics", back_populates="title_principals")


class TitleAkas(Base):
    __tablename__ = "title_akas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titleId = Column(Integer, ForeignKey("title_basics.tconst"))
    ordering = Column(Integer)
    attributes = Column(String(127))
    types = Column(String(31))
    title = Column(Text)
    isOriginalTitle = Column(Boolean)
    language = Column(String(5))
    region = Column(String(5))

    title_basics = relationship("TitleBasics", back_populates="title_akas")


class TitleCrew(Base):
    __tablename__ = "title_crew"

    tconst = Column(Integer, ForeignKey("title_basics.tconst"), primary_key=True)
    writers = Column(Text)
    directors = Column(Text)

    title_basics = relationship("TitleBasics", back_populates="title_crew")


class TitleEpisode(Base):
    __tablename__ = "title_episode"

    tconst = Column(Integer, ForeignKey("title_basics.tconst"), primary_key=True)
    parentTconst = Column(Integer)
    seasonNumber = Column(Integer)
    episodeNumber = Column(Integer)

    title_basics = relationship("TitleBasics", back_populates="title_episode")


class TitleRatings(Base):
    __tablename__ = "title_ratings"

    tconst = Column(Integer, ForeignKey("title_basics.tconst"), primary_key=True)
    averageRating = Column(Float)
    numVotes = Column(Integer)

    title_basics = relationship("TitleBasics", back_populates="title_ratings")


NAME2ORM = {
    NameBasics.__tablename__: NameBasics,
    TitleAkas.__tablename__: TitleAkas,
    TitleBasics.__tablename__: TitleBasics,
    TitleCrew.__tablename__: TitleCrew,
    TitleEpisode.__tablename__: TitleEpisode,
    TitlePrincipals.__tablename__: TitlePrincipals,
    TitleRatings.__tablename__: TitleRatings,
}
