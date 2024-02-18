# pylint: disable=import-error
# pylint: disable=no-name-in-module
"""Pruebas unitarias reservas"""
import unittest
from unittest.mock import patch
from entities.reservation import Reservation


class TestReservation(unittest.TestCase):
    """Pruebas unitarias de reservas."""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.customer_id = "C123"
        self.hotel_id = "H123"
        self.start_date = "2023-01-01"
        self.end_date = "2023-01-05"
        self.reservation = Reservation(self.customer_id, self.hotel_id, self.start_date, self.end_date)

    @patch('services.persistence_json_service.PersistenceService.write_data')
    def test_save_reservation(self,  mock_write_data):
        """Prueba la creación de una nueva reserva."""
        self.reservation.save()
        mock_write_data.assert_called_once()
        args, _ = mock_write_data.call_args
        self.assertIn(self.reservation.reservation_id, args[0])
        reservation_data = args[0][self.reservation.reservation_id]
        self.assertEqual(reservation_data["customer_id"], self.customer_id)
        self.assertEqual(reservation_data["hotel_id"], self.hotel_id)
        self.assertEqual(reservation_data["start_date"], self.start_date)
        self.assertEqual(reservation_data["end_date"], self.end_date)

    @patch('services.persistence_json_service.PersistenceService.write_data')
    @patch('services.persistence_json_service.PersistenceService.read_data', return_value={"1": {"customer_id": "C123", "hotel_id": "H123"}})
    def test_cancel_reservation(self,  mock_read_data, mock_write_data):
        """Prueba la cancelación de una reserva."""
        Reservation.cancel("1")
        mock_write_data.assert_called_once()
        args, _ = mock_write_data.call_args
        self.assertNotIn("some_reservation_id", args[0])


if __name__ == '__main__':
    unittest.main()
