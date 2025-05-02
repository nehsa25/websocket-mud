from utilities.log_telemetry import LogTelemetryUtility


class EventUtility:
    def __init__(self) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)

    @staticmethod
    def get_event_type_id(event):
        return event.value
    
    @staticmethod

    async def send_message(event_object, websocket):
        msg = event_object.to_json()
        await websocket.send(str(msg))
        