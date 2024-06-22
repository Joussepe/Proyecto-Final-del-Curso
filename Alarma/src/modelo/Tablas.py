# src/modelo/Tablas.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.modelo.BaseDeDatos import Base

class Alarma(Base):
    __tablename__ = 'alarmas'

    Id_Alarma = Column(Integer, primary_key=True)
    Hora_Alarma = Column(String, nullable=False)
    Etiqueta = Column(String)
    Sonido_Id = Column(Integer, ForeignKey('sonidos.Id_Sonido'))

    sonido = relationship('Sonido', back_populates='alarmas')


class Sonido(Base):
    __tablename__ = 'sonidos'

    Id_Sonido = Column(Integer, primary_key=True)
    Nombre = Column(String, nullable=False)
    Tipo = Column(String)

    alarmas = relationship('Alarma', back_populates='sonido')
