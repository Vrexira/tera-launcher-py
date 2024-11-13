import json

from .mapping import LAUNCHER_EVENT_CODE, CLIENT_END_CODE


class MessageRouter:
    """Base Message Router class for common message routing functionalities.

    This class provides a foundation for message routing, shared by
    different types of message routers (e.g., IPC and CLI).

    Attributes:
        loader: The loader instance used to log messages and handle exits.
    """
    
    def __init__(self, loader):
        """Initializes the BaseMessageRouter with a loader instance.

        Args:
            loader: An instance of a loader that manages game configurations and actions.
        """
        self.loader = loader  # Reference to the loader instance
    
    def route(self, message_str = "", code = ""):
        """Routes the message to the appropriate handler based on the message string.

        Args:
            message_str: The string representation of the message to be handled.
            code: The integer code associated with the message.
        """
        handler = getattr(self, f"_handle_{message_str}", self._handle_default)
        handler(code, message_str)
    
    def _handle_default(self, code, message_str):
        """Handles unrecognized messages.

        Args:
            code: The integer code associated with the message.
            message_str: The string representation of the message.
        """
        if self.loader.debug:
            self.loader.log(["info", f"Unhandled message: {code} {message_str}"])


class IPCMessageRouter(MessageRouter):
    """IPC Message Router
    Routes messages to the appropriate handler based on the message content.

    This class manages incoming messages and directs them to specific
    handler methods based on the message string.

    Attributes:
        loader (IPCLoader): The loader instance used to log messages and handle exits.
    """
    
    def _handle_ticket(self, code, message_str):
        """Handles ticket-related messages.

        Args:
            code: The integer code associated with the message.
            message_str: The string representation of the message.
        """
        try:
            res = {
                "ticket": self.loader.config.token,
                "result-code": self.loader.config.result_code,
                "result-message": self.loader.config.result_message,
            }
            self.loader.SendMessageToClient("ticket", json.dumps(res))
        
        except Exception as e:
            if self.loader.debug:
                self.loader.log(["error", str(e)])
    
    def _handle_last_svr(self, code, message_str):
        """Handles messages related to the last server.

        Args:
            code: The integer code associated with the message.
            message_str: The string representation of the message.
        """
        try:
            self.loader.SendMessageToClient("last_svr", f"{self.loader.config.last_svr}")
        
        except Exception as e:
            if self.loader.debug:
                self.loader.log(["error", str(e)])
    
    def _handle_char_cnt(self, code, message_str):
        """Handles messages related to character count.

        Args:
            code: The integer code associated with the message.
            message_str: The string representation of the message.
        """
        try:
            self.loader.SendMessageToClient("char_cnt", f"{self.loader.config.char_cnt}")
        
        except Exception as e:
            if self.loader.debug:
                self.loader.log(["error", str(e)])
    
    def _handle_gameEvent(self, code, message_str):
        """Handles game event messages.

        Args:
            code: The integer code associated with the message.
            message_str: The string representation of the message.
        """
        if code == 1001 and self.loader.first:
            self.loader.first = False
        else:
            if self.loader.debug:
                self.loader.log(["info", f"{LAUNCHER_EVENT_CODE.get(code, 'Unknown event')} | {code}"])
    
    def _handle_endPopup(self, code, message_str):
        """Handles end popup messages.

        Args:
            code: The integer code associated with the message.
            message_str: The string representation of the message.
        """
        try:
            code_1 = code
            code_2 = 0
            if code_1 not in CLIENT_END_CODE:
                end_message = f"CLIENT_END_CODE | Unknown Client Ending | {code_1}"
            else:
                if "-" in str(code):
                    ending = str(code).split("-")
                    code_1 = ending[0]
                    code_2 = ending[1]
                elif "," in str(code):
                    ending = str(code).split(",")
                    code_1 = ending[0]
                    code_2 = ending[1]
                end_message = f"CLIENT_END_CODE | {CLIENT_END_CODE[code_1][code_2]} | {code_1}-{code_2}"
            
            if code_1 in {0, 7, 16}:
                self._handle_gameEvent(1001, message_str)
            
            if self.loader.debug:
                self.loader.log(["info", end_message])
            self.loader.exit()
        
        except Exception as e:
            if self.loader.debug:
                self.loader.log(["error", str(e)])
    
    def _handle_csPopup(self, code, message_str):
        """Handles client-side popup messages.

        Args:
            code: The integer code associated with the message.
            message_str: The string representation of the message.
        """
        if self.loader.debug:
            self.loader.log(["info", ["csPopup", code]])
    
    def _handle_promoPopup(self, code, message_str):
        """Handles promotional popup messages.

        Args:
            code: The integer code associated with the message.
            message_str: The string representation of the message.
        """
        if self.loader.debug:
            self.loader.log(["info", ["promoPopup", code]])
    
    def _handle_getWebLinkUrl(self, code, message_str):
        """Handles requests for web link URLs.

        Args:
            code: The integer code associated with the message.
            message_str: The string representation of the message.
        """
        try:
            action = message_str.split("(")[0]
            params = message_str.split("(")[1][:-1].split(",")
            
            lang_id = int(params[0])
            server_id = int(params[1])
            char_id = int(params[2])
            user_id = int(self.loader.config.user_id)
            user_token = self.loader.config.token
            
            url_return = f"{self.loader.config.url}/announce?lang_id={lang_id}&server_id={server_id}&user_id={user_id}&char_id={char_id}&token={user_token}"
            
            if self.loader.debug:
                self.loader.log(["info", [message_str, action, params, url_return]])
            self.loader.SendMessageToClient(message_str, url_return)
        
        except Exception as e:
            if self.loader.debug:
                self.loader.log(["error", str(e)])
