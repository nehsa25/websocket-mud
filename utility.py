import json
from log_utils import LogUtils

class Utility:
    @staticmethod
    async def send_msg(msg, message_type, websocket, logger=None, extra=""):        
        json_msg = { "type": message_type, 'message': msg, 'extra': extra }
        LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
        await websocket.send(json.dumps(json_msg))

