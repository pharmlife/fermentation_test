"""
Logic for defining the database schema

"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    location = Column(String)

    fermentor_list = relationship("Fermentor", back_populates="client")


class FermentorModel(Base):
    __tablename__ = 'fermentor_models'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    fermentor_list = relationship("Fermentor", back_populates="model")


class Fermentor(Base):
    __tablename__ = 'fermentors'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    model_id = Column(Integer, ForeignKey('fermentor_models.id'))
    model = relationship('FermentorModel', back_populates='fermentor_list')

    client_id = Column(Integer, ForeignKey('clients.id'))
    client = relationship('Client', back_populates='fermentor_list')

    process_list = relationship('FermentationProcess', back_populates='fermentor')


class FermentationProcess(Base):
    __tablename__ = "fermentation_processes"

    id = Column(Integer, primary_key=True)
    is_blank = Column(Boolean)

    fermentor_id = Column(Integer, ForeignKey('fermentors.id'))
    fermentor = relationship('Fermentor', back_populates='process_list')

    sample = relationship("FermentationSample", uselist=False, back_populates="process")


class FermentationSample(Base):
    __tablename__ = "fermentation_samples"

    id = Column(Integer, primary_key=True)
    timestamp = Column(String)
    url = Column(String)

    process_id = Column(ForeignKey('fermentation_processes.id'), unique=True)
    process = relationship("FermentationProcess", back_populates='sample')

