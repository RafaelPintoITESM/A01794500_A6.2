"""Pruebas unitarias clientes"""
import unittest
from unittest.mock import patch
from entities.customer import Customer


CUSTOMER_NAME = "John Doe"
CUSTOMER_EMAIL = "johndoe@example.com"


class TestCustomer(unittest.TestCase):
    """"Pruebas unitarias para cliente"""
    def setUp(self):
        """Preparación antes de cada prueba."""
        self.customer = Customer("1", CUSTOMER_NAME, CUSTOMER_EMAIL)

    @patch('services.persistence_json_service.PersistenceService.write_data')
    @patch('services.persistence_json_service.PersistenceService.read_data', return_value={})
    def test_save_new_customer(self, mock_read_data, mock_write_data):
        """Prueba la creación de un nuevo cliente."""
        self.customer.save()
        mock_write_data.assert_called_once()
        mock_read_data.assert_called_once()
        args, _ = mock_write_data.call_args
        self.assertIn("1", args[0])  # Verifica que el cliente se haya agregado al diccionario
        self.assertEqual(args[0]["1"]["name"], CUSTOMER_NAME)
        self.assertEqual(args[0]["1"]["email"], CUSTOMER_EMAIL)

    @patch('services.persistence_json_service.PersistenceService.write_data')
    @patch('services.persistence_json_service.PersistenceService.read_data', return_value={"1": {"name": "John Doe", "email": "johndoe@example.com"}})
    def test_delete_customer(self, mock_read_data, mock_write_data):
        """Prueba la eliminación de un cliente."""
        Customer.delete("1")
        mock_write_data.assert_called_once()
        args, _ = mock_write_data.call_args
        self.assertNotIn("1", args[0])  # Verifica que el cliente se haya eliminado del diccionario

    @patch('services.persistence_json_service.PersistenceService.read_data', return_value={"1": {"name": CUSTOMER_NAME, "email": CUSTOMER_EMAIL}})
    def test_display_customer_info(self, mock_read_data):
        """Prueba la visualización de la información de un cliente."""
        result = Customer.display_customer_info("1")
        mock_read_data.assert_called_once()
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], CUSTOMER_NAME)
        self.assertEqual(result["email"], CUSTOMER_EMAIL)

    @patch('services.persistence_json_service.PersistenceService.write_data')
    def test_update_customer_info(self,  mock_write_data):
        """Prueba la actualización de la información de un cliente."""
        self.customer.update_info(name="Jane Doe", email="janedoe@example.com")
        mock_write_data.assert_called_once()
        args, _ = mock_write_data.call_args
        self.assertIn("1", args[0])
        self.assertEqual(args[0]["1"]["name"], "Jane Doe")
        self.assertEqual(args[0]["1"]["email"], "janedoe@example.com")


if __name__ == '__main__':
    unittest.main()
