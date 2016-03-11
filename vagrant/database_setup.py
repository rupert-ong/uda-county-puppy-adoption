# Configuration code
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Class Code
class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zipCode = Column(String(10))
    website = Column(String)


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    gender = Column(String(6), nullable=False)
    dateOfBirth = Column(Date)
    # picture = Column(String)
    weight = Column(Numeric(10))

    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)

    # One-to-One relationship with PuppyProfile(.puppy)
    profile = relationship(
        "PuppyProfile", uselist=False, back_populates="puppy")


class PuppyProfile(Base):
    __tablename__ = 'puppy_profile'
    id = Column(Integer, primary_key=True)
    picture = Column(String)
    description = Column(String)
    special_needs = Column(String)

    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", back_populates="profile")


# Determine which DB to communicate with...
engine = create_engine('sqlite:///puppyshelter.db')

# Bind engine to the Base class
Base.metadata.create_all(engine)
