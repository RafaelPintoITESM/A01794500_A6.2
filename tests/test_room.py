# pylint: disable=import-error
# pylint: disable=no-name-in-module
"""Pruebas unitarias habitacion"""
import unittest
from entities.room import Room


class TestRoom(unittest.TestCase):
    """Pruebas unitarias habitacion"""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.room = Room(room_id="101", number="101")

    def test_reserve(self):
        """Prueba que una habitación pueda ser reservada correctamente."""
        result = self.room.reserve("2023-01-01", "2023-01-05")
        self.assertTrue(result)
        self.assertTrue(self.room.is_reserved)
        self.assertIn(("2023-01-01", "2023-01-05"), self.room.reservation_dates)

    def test_cancel_reservation(self):
        """Prueba la cancelación de una reserva."""
        # Primero reservamos la habitación para asegurarnos de que hay algo que cancelar
        self.room.reserve("2023-01-01", "2023-01-05")
        result = self.room.cancel_reservation()
        self.assertTrue(result)
        self.assertFalse(self.room.is_reserved)
        self.assertEqual(len(self.room.reservation_dates), 0)

    def test_to_dict(self):
        """Prueba la conversión de la instancia de Room a un diccionario."""
        expected_dict = {
            "room_id": "101",
            "number": "101",
            "is_reserved": False,
            "reservation_dates": []
        }
        self.assertEqual(self.room.to_dict(), expected_dict)


if __name__ == '__main__':
    unittest.main()
