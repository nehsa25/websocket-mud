from utilities.exception import ExceptionUtility
from utilities.log_telemetry import LogTelemetryUtility


class EventUtility:
    def __init__(self) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)

    @staticmethod
    def get_event_type_id(event):
        return event.value

    async def send_message(self, event_object, websocket):
        msg = event_object.to_json()
        self.logger.debug("enter")
        self.logger.debug(f"Sending json: {msg}")
        self.logger.debug("exit")
        try:
            await websocket.send(str(msg))
        except Exception as e:
            self.logger.error(f"Error: {ExceptionUtility.get_exception_information(e)}")
