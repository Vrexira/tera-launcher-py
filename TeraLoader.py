# requires python in 32 bit due to TERA's "TL.exe"

import ctypes
import json
import DynamicLinkLibrary as DLL

from Helper import std_out
from Mapping import CLIENT_END_CODE, LAUNCHER_EVENT_CODE


class Loader:
	def __init__(self, game_str: dict, func: any, debug: bool = False):
		self.url = game_str['url']
		self.debug = debug
		self.game_str = game_str
		self.first = True
		self.launcher_dll = DLL
		self.exit = func

	def LaunchGame(self):
		sls = ctypes.c_char_p((self.url+self.game_str['sls']).encode())
		game_str = ctypes.c_char_p(json.dumps(self.game_str).encode())
		self.launcher_dll.LaunchGame(sls, game_str)

	def RegisterMessageListener(self):
		MessageListenerDelegate = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int)
		mlDelegate = MessageListenerDelegate(self.MessageListener)
		mlPointer = ctypes.cast(mlDelegate, ctypes.c_void_p)
		self.launcher_dll.RegisterMessageListener(mlPointer)

	def SendMessageToClient(self, responseTo, Message):
		res = ctypes.c_char_p(responseTo.encode())
		msg = ctypes.c_char_p(Message.encode())
		self.launcher_dll.SendMessageToClient(res, msg)

	def MessageListener(self, message: bytes, code: int):
		if self.debug: std_out(message, code)
		message_str = message.decode()
		code_int = int(code)

		if message_str == "ticket":
			res = {
				"ticket": self.game_str['token'],
				"result-code": self.game_str['result-code'],
				"result-message": self.game_str['result-message']
			}
			self.SendMessageToClient("ticket", json.dumps(res))

		elif message_str == "last_svr":
			# Todo: Change to get updated from API
			self.SendMessageToClient("last_svr", f"{self.game_str['last_svr']}")

		elif message_str == "char_cnt":
			# Todo: Change to get updated from API
			self.SendMessageToClient("char_cnt", f"{self.game_str['char_cnt']}")

		elif message_str == "gameEvent":
			if code_int == 1001 and self.first:
				self.first = False
			else:
				std_out(f"{LAUNCHER_EVENT_CODE[code_int]} | {code_int}")

		elif message_str == "endPopup":
			code_1 = code_int
			code_2 = 0
			if code_1 not in CLIENT_END_CODE:
				end_message = f"CLIENT_END_CODE | Unknown Client Ending | {code_1}"
			else:
				if "-" in str(code_int):
					ending = str(code_int).split("-")
					code_1 = ending[0]
					code_2 = ending[1]
				elif "," in str(code_int):
					ending = str(code_int).split(",")
					code_1 = ending[0]
					code_2 = ending[1]
				end_message = f"CLIENT_END_CODE | {CLIENT_END_CODE[code_1][code_2]} | {code_1}-{code_2}"

			if code_1 == 0 or code_1 == 7 or code_1 == 16:
				self.MessageListener(b"gameEvent", 1001)
			std_out(end_message)
			self.exit()

		elif message_str == "csPopup":
			std_out(message_str, code)

		elif message_str == "promoPopup":
			std_out(message_str, code)

		elif "getWebLinkUrl" in message_str:
			action = message_str.split("(")[0]
			params = message_str.split("(")[1][:-1].split(",")

			web_id = int(params[0])
			server_id = int(params[1])
			char_id = int(params[2])
			user_id = int(self.game_str['user_id'])
			user_token = self.game_str['token']

			url_return = ""

			if web_id == 200 and server_id == 2800:
				url_return = f"{self.url}/announce/0x0001?server_id={server_id}&user_id={user_id}&char_id={char_id}&token={user_token}"

			elif web_id == 210 and server_id == 2801:
				url_return = f"{self.url}/announce/0x0002?server_id={server_id}&user_id={user_id}&char_id={char_id}&token={user_token}"

			elif web_id == 230 and server_id == 2801:
				url_return = f"{self.url}/announce/0x0003?server_id={server_id}&user_id={user_id}&char_id={char_id}&token={user_token}"

			if self.debug: std_out([message_str, action, params, url_return])
			self.SendMessageToClient(message_str, url_return)
