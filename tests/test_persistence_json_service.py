# pylint: disable=import-error
"""Pruebas unitarias para persistencia en json"""
import unittest
from unittest.mock import patch, mock_open
import json
from services.persistence_json_service import PersistenceService


class TestPersistenceService(unittest.TestCase):
    """Pruebas unitarias para persistencia en json"""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.file_path = "test_data"
        self.persistence_service = PersistenceService(self.file_path)

    @patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
    def test_read_data_success(self, mock_file):
        """Prueba la lectura exitosa de datos desde un archivo JSON."""
        result = self.persistence_service.read_data()
        self.assertEqual(result, {"key": "value"})
        mock_file.assert_called_once_with(f"repository/{self.file_path}.json", 'r', encoding='utf-8')

    @patch("builtins.open", new_callable=mock_open, read_data='')
    @patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0))
    def test_read_data_json_decode_error(self, mock_json_load, mock_file):
        """Prueba el manejo de un JSONDecodeError al leer datos."""
        result = self.persistence_service.read_data()
        self.assertEqual(result, {})
        mock_file.assert_called_once()
        mock_json_load.assert_called_once()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_data_file_not_found_error(self, mock_file):
        """Prueba el manejo de un FileNotFoundError al leer datos."""
        result = self.persistence_service.read_data()
        self.assertEqual(result, {})
        mock_file.assert_called_once_with(f"repository/{self.file_path}.json", 'r', encoding='utf-8')

    @patch("builtins.open", new_callable=mock_open)
    def test_write_data(self, mock_file):
        """Prueba la escritura exitosa de datos en un archivo JSON."""
        test_data = {"new_key": "new_value"}
        self.persistence_service.write_data(test_data)
        mock_file.assert_called_once_with(f"repository/{self.file_path}.json", 'w', encoding='utf-8')
        # Asegurar que se llama a write, pero sin especificar exactamente qué se escribe cada vez.
        self.assertTrue(mock_file().write.called)


if __name__ == '__main__':
    unittest.main()
