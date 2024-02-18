# pylint: disable=import-error
""" Representacion de cliente y su persistencia abstraida """
from services.persistence_json_service import PersistenceService


class Customer:
    """ Representacion de cliente y su persistencia abstraida """
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.persistence_service = PersistenceService(Customer.store_name())

    @staticmethod
    def store_name():
        """Retorna nombre del store"""
        return "customers"

    def save(self):
        """Guarda un nuevo cliente o actualiza uno existente en el archivo JSON."""
        customers = self.persistence_service.read_data()
        customers[self.customer_id] = {
            "name": self.name,
            "email": self.email
        }
        self.persistence_service.write_data(customers)

    @staticmethod
    def delete(customer_id):
        """Elimina un cliente por su ID."""
        service = PersistenceService(Customer.store_name())
        customers = service.read_data()
        if customer_id in customers:
            del customers[customer_id]
            service.write_data(customers)

    @staticmethod
    def get_customers():
        """Obtiene todos los clientes."""
        service = PersistenceService(Customer.store_name())
        return service.read_data()

    @staticmethod
    def display_customer_info(customer_id):
        """Muestra la información de un cliente específico."""
        customers = Customer.get_customers()
        return customers.get(customer_id, None)

    def update_info(self, name=None, email=None):
        """Actualiza la información de un cliente."""
        if name:
            self.name = name
        if email:
            self.email = email
        self.save()
