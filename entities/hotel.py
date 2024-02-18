# pylint: disable=import-error
from services.persistence_json_service import PersistenceService


class Hotel:
    """ Representacion de hotel y su persistencia abstraida """
    def __init__(self, hotel_id, name, address, rooms=None):
        self.hotel_id = hotel_id
        self.name = name
        self.address = address
        self.rooms = rooms if rooms is not None else []
        self.persistence_service = PersistenceService(self.store_name())

    @staticmethod
    def store_name():
        """Retorna el nombre del almacenamiento."""
        return "hotels"

    def add_room(self, room):
        """Agrega una habitación al hotel."""
        self.rooms.append(room)

    def reserve_room(self, room_id, start_date, end_date):
        """Busca una habitación por ID y la reserva si está disponible."""
        for room in self.rooms:
            if room.room_id == room_id and not room.is_reserved:
                success = room.reserve(start_date, end_date)  # Asume esta función en Room
                if success:
                    self.save()  # Actualiza la información del hotel con la reserva
                    return True
        return False

    def cancel_room_reservation(self, room_id):
        """Busca una habitación por ID y cancela su reserva."""
        for room in self.rooms:
            if room.room_id == room_id:
                success = room.cancel_reservation()  # Asume esta función en Room
                if success:
                    self.save()  # Actualiza la información del hotel tras cancelar la reserva
                    return True
        return False

    def save(self):
        """Guarda o actualiza la información del hotel, incluidas sus habitaciones."""
        hotels = self.persistence_service.read_data()
        hotel_data = {
            "name": self.name,
            "address": self.address,
            "rooms": [room.to_dict() for room in self.rooms]  # Asume que Room tiene un método to_dict()
        }
        hotels[self.hotel_id] = hotel_data
        self.persistence_service.write_data(hotels)

    @staticmethod
    def delete(hotel_id):
        """Elimina un hotel por su ID."""
        service = PersistenceService(Hotel.store_name())
        hotels = service.read_data()
        if hotel_id in hotels:
            del hotels[hotel_id]
            service.write_data(hotels)

    @classmethod
    def get_hotels(cls):
        """Obtiene todos los hoteles."""
        service = PersistenceService(cls.store_name())
        return service.read_data()

    @classmethod
    def display_info(cls, hotel_id):
        """Muestra la información de un hotel específico."""
        hotels = cls.get_hotels()
        return hotels.get(hotel_id, None)

    def update_info(self, name=None, address=None):
        """Actualiza la información del hotel."""
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address
        self.save()
