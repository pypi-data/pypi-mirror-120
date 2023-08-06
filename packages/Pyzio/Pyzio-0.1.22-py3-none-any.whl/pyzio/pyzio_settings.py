from abc import ABC, abstractmethod
from typing import List, Tuple


class PyzioSettings(ABC):

	@abstractmethod
	def brainer_host(self) -> str:
		pass

	@abstractmethod
	def mqtt_host(self) -> str:
		pass

	@abstractmethod
	def mqtt_port(self) -> int:
		pass

	@abstractmethod
	def printer_id(self) -> str:
		pass

	@abstractmethod
	def pairing_id(self) -> str:
		pass

	@abstractmethod
	def candidate_id(self) -> str:
		pass

	@abstractmethod
	def printer_secret(self) -> str:
		pass

	@abstractmethod
	def get_sensors(self) -> List[Tuple[str, str]]:
		pass

	@abstractmethod
	def set_printer_id(self, id: str) -> str:
		pass

	@abstractmethod
	def set_printer_secret(self, secret: str) -> str:
		pass

	@abstractmethod
	def set_sensors(self, sensors: List[Tuple[str, str]]) -> None:
		pass

	@abstractmethod
	def save(self) -> None:
		pass

	@abstractmethod
	def print_file_storage(self) -> str:
		pass
