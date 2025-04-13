import random
from dontcheckin import Secrets
from log_utils import LogUtils
import google.generativeai as genai
from utility import Utility

class NpcDialog:
    """Responsible for interacting with Gemeni's dialog system.
    
    Attributes:
        logger: A logger object.
    """
    logger = None
    key = None
    seed = None
    def __init__(self, seed, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing GeminiAPI() class", self.logger)            
        self.key = Secrets.GeminiAPIKey
        self.seed = seed

    def __init__(self, logger):
        """Inits Dialog with logger."""
        self.logger = logger
        LogUtils.debug(f"Initializing Dialog() class", logger)
        
    async def intelligize_npc(self, npc, room_description, current_interests, last_message):
        genai.configure(api_key=Secrets.GeminiAPIKey)            
        model = genai.GenerativeModel('gemini-1.5-flash',)
        msg = f"""You are a {npc.name} {npc.title}. More about you: {npc.description}.  You live in the world of 
        {Utility.WORLD_NAME} in the town of Smee. Your general interests are \"{npc.interests}\".  
        You are in the room \"{room_description}\" and the following events are currently happening: \"{current_interests}\".  
        Pick only one thing to reply to and it shoud be something that is in your general interest if possible. Reply as if you were {npc.name}."""
        
        if last_message is not None and last_message.response_time is None:
            msg += f" The latest thing said in the room was \"{last_message.message}\" by \"{last_message.player_name}\".  Reply to this if you can and if this player is still in the room."
        response =  model.generate_content(msg)
        
        response_options = [
            f"{npc.get_full_name()} says {response.text.strip('\"')}",
            f"{npc.get_full_name()} mentions {response.text.strip('\"')}",
            f"{npc.get_full_name()} states {response.text.strip('\"')}",]
        return random.choice(response_options)