# pylint: disable=import-error
"""Modulo de reservas."""
import uuid  # Para generar IDs únicos para cada reserva
from services.persistence_json_service import PersistenceService


class Reservation:
    """ Representacion de reservas y su persistencia abstraida """
    def __init__(self, customer_id, hotel_id, start_date, end_date):
        self.reservation_id = str(uuid.uuid4())  # Genera un ID único
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.start_date = start_date
        self.end_date = end_date
        self.persistence_service = PersistenceService(self.store_name())

    @staticmethod
    def store_name():
        """Retorna el nombre del almacenamiento."""
        return "hotels"

    def save(self):
        """Crea una nueva reserva."""
        reservations = self.persistence_service.read_data()
        reservations[self.reservation_id] = {
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
        self.persistence_service.write_data(reservations)

    @staticmethod
    def cancel(reservation_id):
        """Cancela una reserva."""
        service = PersistenceService(Reservation.store_name())
        reservations = service.read_data()
        if reservation_id in reservations:
            del reservations[reservation_id]
            service.write_data(reservations)
