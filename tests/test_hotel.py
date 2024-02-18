# pylint: disable=import-error
# pylint: disable=no-name-in-module
# pylint: disable=no-member
"""Pruebas unitarias para hotel"""
import unittest
from unittest.mock import patch
from entities.hotel import Hotel
from entities.room import Room


HOTEL_NAME = "Hotel Prueba"
HOTEL_ADDRESS = "Calle Ejemplo, 123"


class TestHotel(unittest.TestCase):
    """Pruebas unitarias para hotel"""
    def setUp(self):
        """Preparación antes de cada prueba."""
        self.hotel = Hotel("1", HOTEL_NAME, HOTEL_ADDRESS)
        self.room = Room("101", "101")

    def test_add_room(self):
        """Prueba que se pueda agregar una habitación al hotel."""
        self.hotel.add_room(self.room)
        self.assertIn(self.room, self.hotel.rooms)
        self.assertEqual(len(self.hotel.rooms), 1)

    @patch('services.persistence_json_service.PersistenceService.write_data')
    @patch('services.persistence_json_service.PersistenceService.read_data', return_value={})
    def test_reserve_room(self, mock_read_data, mock_write_data):
        """Prueba reservar una habitación en el hotel."""
        self.hotel.add_room(self.room)
        result = self.hotel.reserve_room("101", "2023-01-01", "2023-01-05")
        self.assertTrue(result)
        self.assertTrue(self.room.is_reserved)
        self.assertEqual(self.room.reservation_dates, [("2023-01-01", "2023-01-05")])
        mock_write_data.assert_called_once()

    @patch('services.persistence_json_service.PersistenceService.write_data')
    def test_cancel_room_reservation(self, mock_write_data):
        """Prueba la cancelación de una reserva de habitación."""
        self.hotel.add_room(self.room)
        self.room.reserve("2023-01-01", "2023-01-05")  # Reservar directamente para la prueba
        result = self.hotel.cancel_room_reservation("101")
        self.assertTrue(result)
        self.assertFalse(self.room.is_reserved)
        self.assertEqual(self.room.reservation_dates, [])
        mock_write_data.assert_called_once()

    @patch('services.persistence_json_service.PersistenceService.write_data')
    def test_save_hotel(self,  mock_write_data):
        """Prueba la persistencia de la información del hotel."""
        self.hotel.save()
        mock_write_data.assert_called_once()

    def test_display_info(self):
        """Prueba la visualización de la información de un hotel."""
        hotel_info = Hotel.display_info("1")
        self.assertIsNotNone(hotel_info)
        self.assertEqual(hotel_info["name"], "Hotel Sol")

    @patch('services.persistence_json_service.PersistenceService.write_data')
    @patch('services.persistence_json_service.PersistenceService.read_data', return_value={"1": {"name": "Hotel Sol", "address": "Calle Sol, 123", "rooms": 2, "reservations": {"res2": "cust2"}}})
    def test_delete_hotel(self, mock_read_data, mock_write_data):
        """Prueba para eliminar un hotel"""
        Hotel.delete("1")
        mock_write_data.assert_called_once_with({})

    @patch('services.persistence_json_service.PersistenceService.read_data', return_value={"1": {"name": "Hotel Sol", "address": "Calle Sol, 123", "rooms": 2, "reservations": {"res2": "cust2"}}})
    def test_get_hotels(self, mock_read_data):
        """Prueba para obtenes todos los hoteles"""
        hotels = Hotel.get_hotels()
        self.assertIn("1", hotels)
        self.assertEqual(hotels["1"]["name"], "Hotel Sol")

    @patch('services.persistence_json_service.PersistenceService.write_data')
    @patch('services.persistence_json_service.PersistenceService.read_data', return_value={"1": {"name": "Hotel Sol", "address": "Calle Sol, 123", "rooms": 2, "reservations": {"res2": "cust2"}}})
    def test_update_info(self, mock_read_data, mock_write_data):
        """Prueba para actualizar hotel"""
        mock_read_data.return_value = {"1": {"name": HOTEL_NAME, "address": HOTEL_ADDRESS, "rooms": []}}
        self.hotel.update_info(name="Hotel Actualizado", address="Calle Actualizada, 456")
        mock_write_data.assert_called_once()
        args, _ = mock_write_data.call_args
        self.assertEqual(args[0]["1"]["name"], "Hotel Actualizado")
        self.assertEqual(args[0]["1"]["address"], "Calle Actualizada, 456")

    @patch('services.persistence_json_service.PersistenceService.write_data')
    @patch('services.persistence_json_service.PersistenceService.read_data', return_value={})
    def test_reserve_room_failure(self, mock_read_data, mock_write_data):
        """Prueba para reservar fallando"""
        self.hotel.add_room(self.room)
        self.room.reserve("2023-01-01", "2023-01-05")  # La habitación ya está reservada
        result = self.hotel.reserve_room("101", "2023-01-06", "2023-01-10")  # Intenta reservar nuevamente
        self.assertFalse(result)  # La reserva debería fallar


if __name__ == '__main__':
    unittest.main()
