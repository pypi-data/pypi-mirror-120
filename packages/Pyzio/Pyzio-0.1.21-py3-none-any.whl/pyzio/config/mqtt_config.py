from ..pyzio_settings import PyzioSettings


class MQTTConfig:

	def __init__(self, settings: PyzioSettings):
		self._settings = settings

	def host(self) -> str:
		return self._settings.mqtt_host()

	def port(self) -> int:
		return self._settings.mqtt_port()
