from sqlalchemy import Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class NameBasics(Base):
    __tablename__ = "name_basics"

    nconst = Column(Integer, primary_key=True)
    knownForTitles = Column(Text)
    primaryName = Column(Text)
    primaryProfession = Column(Text)
    deathYear = Column(Integer)
    birthYear = Column(Integer)


class TitleAkas(Base):
    __tablename__ = "title_akas"

    titleId = Column(Integer, primary_key=True)
    ordering = Column(Integer)
    attributes = Column(String(127))
    types = Column(String(31))
    title = Column(Text)
    isOriginalTitle = Column(Integer)  # BOOLEAN as INTEGER in SQLite
    language = Column(String(5))
    region = Column(String(5))


class TitleBasics(Base):
    __tablename__ = "title_basics"

    tconst = Column(Integer, primary_key=True)
    primaryTitle = Column(Text)
    originalTitle = Column(Text)
    titleType = Column(String(16))
    isAdult = Column(Integer)  # BOOLEAN as INTEGER in SQLite
    startYear = Column(Integer)
    endYear = Column(Integer)
    runtimeMinutes = Column(Integer)
    genres = Column(Text)


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


class TitlePrincipals(Base):
    __tablename__ = "title_principals"

    tconst = Column(Integer, primary_key=True)
    nconst = Column(Integer, primary_key=True)
    ordering = Column(Integer)
    job = Column(String(1024))
    category = Column(String(64))
    characters = Column(String(1024))


class TitleRatings(Base):
    __tablename__ = "title_ratings"

    tconst = Column(Integer, primary_key=True)
    averageRating = Column(Float)
    numVotes = Column(Integer)
