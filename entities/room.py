"""Modulo de reservas."""


class Room:
    """ Representacion de habitacion y su persistencia abstraida """
    def __init__(self, room_id, number, is_reserved=False, reservation_dates=None):
        self.room_id = room_id
        self.number = number
        self.is_reserved = is_reserved
        self.reservation_dates = reservation_dates or []

    def reserve(self, start_date, end_date):
        """ metodo para reservar habitacion """
        if not self.is_reserved:
            self.is_reserved = True
            self.reservation_dates.append((start_date, end_date))
            return True
        return False

    def cancel_reservation(self):
        """ metodo para cancelar reserva de habitacion """
        if self.is_reserved:
            self.is_reserved = False
            self.reservation_dates.clear()
            return True
        return False

    def to_dict(self):
        """Convierte la instancia de Room en un diccionario para su serialización."""
        return {
            "room_id": self.room_id,
            "number": self.number,
            "is_reserved": self.is_reserved,
            "reservation_dates": self.reservation_dates
        }
