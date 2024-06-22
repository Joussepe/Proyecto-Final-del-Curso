# tests/TestAlarma.py

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.modelo.Tablas import Base, Alarma, Sonido
from src.modelo.BaseDeDatos import DATABASE_URL, SessionLocal
from src.logica.AlarmaCRUD import AlarmaCRUD

class TestAlarma(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Configurar la conexión a la base de datos SQLite en disco
        cls.engine = create_engine(DATABASE_URL)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        # Crear todas las tablas en la base de datos
        Base.metadata.create_all(bind=cls.engine)

    def setUp(self):
        # Crear una nueva instancia de AlarmaCRUD para cada prueba
        self.alarma_crud = AlarmaCRUD(self.session)

        # Crear algunos sonidos de prueba
        sonido1 = Sonido(Nombre='Ringtone1', Tipo='mp3')
        sonido2 = Sonido(Nombre='Ringtone2', Tipo='wav')
        self.session.add_all([sonido1, sonido2])
        self.session.commit()

    def tearDown(self):
        # Limpiar la sesión después de cada prueba
        self.session.rollback()

    def test_create_alarma(self):
        # Simular entrada de datos por parte del usuario
        hora = input("Hora de la alarma (HH:MM): ")
        etiqueta = input("Etiqueta de la alarma: ")
        sonido_id = int(input("ID del sonido (1 o 2): "))

        alarma = self.alarma_crud.create_alarma(hora, etiqueta, sonido_id)
        self.assertIsNotNone(alarma.Id_Alarma)
        self.assertEqual(alarma.Hora_Alarma, hora)
        self.assertEqual(alarma.Etiqueta, etiqueta)

    # Otros métodos de prueba aquí

    @classmethod
    def tearDownClass(cls):
        # Limpiar y cerrar la sesión después de todas las pruebas
        cls.session.close()
        cls.engine.dispose()

if __name__ == '__main__':
    unittest.main()
