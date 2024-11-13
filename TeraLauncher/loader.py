# requires python in 32 bit due to TERA's "TL.exe"

import ctypes
import json
import os

from .dll import DynamicLinkLibrary as DLL
from .config import GameConfig
from .router import IPCMessageRouter


class IPCLoader:
    """
    A loader for launching games via inter-process communication (IPC).

    This class manages the game launch process using a DLL for game integration,
    listens for messages from the game, and routes them to appropriate handlers
    via the MessageRouter. It facilitates communication between the game and the
    client application.

    Attributes:
        config (GameConfig): The configuration object containing TERA game settings.
        log (callable): The logging function for outputting messages.
        debug (bool): Flag indicating whether debugging is enabled.
        first (bool): A flag indicating whether this is the first message received.
        launcher_dll (CDLL): A reference to the game launcher DLL for IPC.
        exit (callable): The function to call for exiting the application.
        router (IPCMessageRouter): The MessageRouter instance for handling messages.
    """
    
    def __init__(self, game_config: GameConfig, func: any, logger: any, debug: bool = False):
        """Initializes the IPCLoader with game configuration and logger.

        Args:
            game_config: An instance of GameConfig containing game configuration details.
            func: A function to call for exiting the loader.
            logger: A logger instance for logging messages.
            debug: A boolean indicating whether to enable debug logging.
        """
        self.config = game_config
        self.log = logger
        self.debug = debug
        self.first = True
        self.launcher_dll = DLL
        self.exit = func
        self.router = IPCMessageRouter(self)
    
    def LaunchGame(self, app_dir = None):
        """Launches the game using the provided configuration and DLL interface."""
        try:
            work_dir = os.getcwd()
            print(os.getcwd())
            if app_dir is not None:
                os.chdir(app_dir)
                print(os.getcwd())
            sls = ctypes.c_char_p((self.config.url + self.config.sls).encode())
            
            game_dict = self.config.__dict__
            game_dict["result-code"] = 200
            game_dict["result-message"] = "OK"
            game_string = json.dumps(game_dict)
            
            game_str = ctypes.c_char_p(game_string.encode())
            self.launcher_dll.LaunchGame(sls, game_str)
            
            if app_dir is not None:
                os.chdir(work_dir)
            
            return int(0)
        
        except Exception as e:
            return str(e)
    
    def RegisterMessageListener(self):
        """Registers the message listener with the game's DLL for receiving messages."""
        MessageListenerDelegate = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int)
        mlDelegate = MessageListenerDelegate(self.MessageListener)
        mlPointer = ctypes.cast(mlDelegate, ctypes.c_void_p)
        self.launcher_dll.RegisterMessageListener(mlPointer)
    
    def SendMessageToClient(self, responseTo: str, Message: str):
        """Sends a message to the client through the game's DLL interface.

        Args:
            responseTo: The response identifier for the message.
            Message: The message content to be sent to the client.
        """
        res = ctypes.c_char_p(responseTo.encode())
        msg = ctypes.c_char_p(Message.encode())
        self.launcher_dll.SendMessageToClient(res, msg)
    
    def MessageListener(self, message: bytes, code: int):
        """Processes incoming messages and routes them to the appropriate handler.

        Args:
            message: The byte-encoded message received from the client.
            code: The integer code associated with the message.
        """
        message_str = message.decode()
        self.router.route(message_str, code)
