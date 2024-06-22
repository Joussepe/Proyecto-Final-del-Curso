# src/logica/AlarmaCRUD.py

from sqlalchemy.orm import Session
from src.modelo.Tablas import Alarma

class AlarmaCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create_alarma(self, hora: str, etiqueta: str, sonido_id: int):
        nueva_alarma = Alarma(Hora_Alarma=hora, Etiqueta=etiqueta, Sonido_Id=sonido_id)
        self.session.add(nueva_alarma)
        self.session.commit()
        return nueva_alarma

    def read_alarma(self, alarma_id: int):
        return self.session.query(Alarma).filter_by(Id_Alarma=alarma_id).first()

    def update_alarma(self, alarma_id: int, nueva_hora: str, nueva_etiqueta: str):
        alarma = self.session.query(Alarma).filter_by(Id_Alarma=alarma_id).first()
        if alarma:
            alarma.Hora_Alarma = nueva_hora
            alarma.Etiqueta = nueva_etiqueta
            self.session.commit()
        return alarma

    def delete_alarma(self, alarma_id: int):
        alarma = self.session.query(Alarma).filter_by(Id_Alarma=alarma_id).first()
        if alarma:
            self.session.delete(alarma)
            self.session.commit()
        return alarma


