from log_utils import LogUtils

# five gods
class Gods:    
    logger = None    
    
    class Technolegy:
        logger = None
        god_name = "Patton"
        description = "We don't believe in fairies."
        devoption_levels = [
            "high magic resistance",
            "can use high-tech items",
            "can \"think\" their way past locked doors/barriers"         
        ]
        def __init__(self, logger):
            self.logger = logger
            LogUtils.debug(f"Initializing Merchant() class", self.logger)
          
        
    class Merchant:
        logger = None
        god_name = "Patton"
        description = "Murder is never the answer.  It's bad for business."
        devoption_levels = [
            "better prices",
            "better drops",
            "better lockpicking"            
        ]
        def __init__(self, logger):
            self.logger = logger
            LogUtils.debug(f"Initializing Merchant() class", self.logger)
        
    class Nature:
        logger = None
        god_name = "Feyre"
        description = "God of Nature.  Murder is a part of the circle of life."
        devotion_levels = [
            "can track animals",
            "animals will not attack you",
            "can create ents",
            "better animal drops"            
        ]
        def __init__(self, logger):
            self.logger = logger
            LogUtils.debug(f"Initializing Nature() class", self.logger)

    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug(f"Initializing Gods() class", self.logger)
    
                
            