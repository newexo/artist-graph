from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NameBasics(Base):
    __tablename__ = "name_basics"

    nconst = Column(Integer, primary_key=True, index=True)
    knownForTitles = Column(Text)
    primaryName = Column(Text)
    primaryProfession = Column(Text)
    deathYear = Column(Integer)
    birthYear = Column(Integer)


class TitleBasics(Base):
    __tablename__ = "title_basics"

    tconst = Column(Integer, primary_key=True, index=True)
    primaryTitle = Column(Text)
    originalTitle = Column(Text)
    titleType = Column(String(16))
    isAdult = Column(Boolean)
    startYear = Column(Integer)
    endYear = Column(Integer)
    runtimeMinutes = Column(Integer)
    genres = Column(Text)


class TitlePrincipals(Base):
    __tablename__ = "title_principals"

    id = Column(Integer, primary_key=True, autoincrement=True)

    tconst = Column(Integer)
    nconst = Column(Integer)

    ordering = Column(Integer)
    job = Column(String(1024))
    category = Column(String(64))
    characters = Column(String(1024))


class TitleAkas(Base):
    __tablename__ = "title_akas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titleId = Column(Integer)
    ordering = Column(Integer)
    attributes = Column(String(127))
    types = Column(String(31))
    title = Column(Text)
    isOriginalTitle = Column(Boolean)
    language = Column(String(5))
    region = Column(String(5))


class TitleCrew(Base):
    __tablename__ = "title_crew"

    tconst = Column(Integer, primary_key=True)
    writers = Column(Text)
    directors = Column(Text)


class TitleEpisode(Base):
    __tablename__ = "title_episode"

    tconst = Column(Integer, primary_key=True)
    parentTconst = Column(Integer)
    seasonNumber = Column(Integer)
    episodeNumber = Column(Integer)


class TitleRatings(Base):
    __tablename__ = "title_ratings"

    tconst = Column(Integer, primary_key=True)
    averageRating = Column(Float)
    numVotes = Column(Integer)


class NConstTemp(Base):
    __tablename__ = "nconst_temp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nconst = Column(Integer, index=True)


class TConstTemp(Base):
    __tablename__ = "tconst_temp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tconst = Column(Integer, index=True)


NAME2ORM = {
    NameBasics.__tablename__: NameBasics,
    TitleAkas.__tablename__: TitleAkas,
    TitleBasics.__tablename__: TitleBasics,
    TitleCrew.__tablename__: TitleCrew,
    TitleEpisode.__tablename__: TitleEpisode,
    TitlePrincipals.__tablename__: TitlePrincipals,
    TitleRatings.__tablename__: TitleRatings,
}
