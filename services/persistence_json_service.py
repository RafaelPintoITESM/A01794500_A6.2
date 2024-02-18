"""Modulo de Servicio para persistir en archivos json"""
import json
from typing import Dict


class PersistenceService:
    """Servicio para persistir en archivos json"""
    def __init__(self, file_path: str):
        self.file_path = f"repository/{file_path}.json"

    def read_data(self) -> Dict:
        """Lee datos del archivo JSON."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}

    def write_data(self, data: Dict):
        """Escribe datos al archivo JSON."""
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
