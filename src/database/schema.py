"""
Logic for defining the database schema

"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Client(Base):
    __tablename__ = 'Clients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

    fermentor_list = relationship("Fermentor", back_populates="client")


class FermentorModel(Base):
    __tablename__ = 'Models'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    fermentor_list = relationship("Fermentor", back_populates="model")


class Fermentor(Base):
    __tablename__ = 'Fermentors'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    model_id = Column(Integer, ForeignKey('Models.id'))
    model = relationship('FermentorModel', back_populates='fermentor_list')

    client_id = Column(Integer, ForeignKey('Clients.id'))
    client = relationship('Client', back_populates='fermentor_list')

    process_list = relationship('FermentationProcess', back_populates='fermentor')


class FermentationProcess(Base):
    __tablename__ = "Processes"

    id = Column(Integer, primary_key=True)
    is_blank = Column(Boolean)

    fermentor_id = Column(Integer, ForeignKey('Fermentors.id'))
    fermentor = relationship('Fermentor', back_populates='process_list')

    sample = relationship("FermentationSample", uselist=False, back_populates="process")


class FermentationSample(Base):
    __tablename__ = "Samples"

    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    url = Column(String)

    process_id = Column(ForeignKey('Processes.id'), unique=True)
    process = relationship("FermentationProcess", back_populates='sample')

