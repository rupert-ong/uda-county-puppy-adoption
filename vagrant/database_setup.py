# Configuration code
from sqlalchemy import Column, create_engine, ForeignKey, Integer, String, Date, Numeric, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Associative Table for many-to-many relationship (Puppy and Adopter)
puppies_adopters_table = Table(
    'puppies_adopters', Base.metadata,
    Column('puppy_id', ForeignKey('puppy.id'), primary_key=True),
    Column('adopter_id', ForeignKey('adopter.id'), primary_key=True))


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
    current_occupancy = Column(Integer, nullable=False)
    maximum_capacity = Column(Integer, nullable=False)


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

    # Many-to-Many relationship with Adopter(.puppies)
    adopters = relationship(
        "Adopter", secondary=puppies_adopters_table, back_populates='puppies')


class PuppyProfile(Base):
    __tablename__ = 'puppy_profile'
    id = Column(Integer, primary_key=True)
    picture = Column(String)
    description = Column(String)
    special_needs = Column(String)

    puppy_id = Column(Integer, ForeignKey('puppy.id'))
    puppy = relationship("Puppy", back_populates="profile")


class Adopter(Base):
    __tablename__ = 'adopter'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    # Many-to-Many relationship with Puppy(.adopters)
    puppies = relationship(
        'Puppy', secondary=puppies_adopters_table, back_populates='adopters')

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


# Determine which DB to communicate with...
engine = create_engine('sqlite:///puppyshelter.db')

# Bind engine to the Base class
Base.metadata.create_all(engine)
