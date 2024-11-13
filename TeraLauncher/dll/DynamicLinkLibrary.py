# requires pywin32==306

import ctypes
import time

from typing import Any
from helper import std_out
from win32con import IDC_ARROW, IDI_APPLICATION, CS_HREDRAW, CS_VREDRAW, WS_EX_APPWINDOW, WS_OVERLAPPEDWINDOW, MB_ICONERROR, MB_OK, WM_COPYDATA


LAUNCHER_CLASS = "EME.LauncherWnd"
LAUNCHER_WINDOW = LAUNCHER_CLASS

TlExePath = ctypes.create_unicode_buffer(260)
TicketStr = ctypes.create_string_buffer(1024)
LastSvrStr = ctypes.create_string_buffer(1024)
CharCntStr = ctypes.create_string_buffer(1024)
SlsUrl: str = ""
GameString: str = ""
WebLinkUrlStr: str = ""
Hello: bool = False
Sls: bool = False
GameStr: bool = False
Ticket: bool = False
LastSvr: bool = False
CharCnt: bool = False
ClientTerminated: bool = False
WebLinkUrl: bool = False
cds: Any = None
hWndProc: Any = None
uMsgProc: Any = None
wParamProc: Any = None
lParamProc: Any = None
MessageListener: Any = None


WNDPROC = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_void_p)

class STARTUPINFO(ctypes.Structure):
	_fields_ = [
		("cb", ctypes.c_uint32),
		("lpReserved", ctypes.c_void_p),
		("lpDesktop", ctypes.c_void_p),
		("lpTitle", ctypes.c_void_p),
		("dwX", ctypes.c_uint32),
		("dwY", ctypes.c_uint32),
		("dwXSize", ctypes.c_uint32),
		("dwYSize", ctypes.c_uint32),
		("dwXCountChars", ctypes.c_uint32),
		("dwYCountChars", ctypes.c_uint32),
		("dwFillAttribute", ctypes.c_uint32),
		("dwFlags", ctypes.c_uint32),
		("wShowWindow", ctypes.c_uint16),
		("cbReserved2", ctypes.c_uint16),
		("lpReserved2", ctypes.POINTER(ctypes.c_uint8)),
		("hStdInput", ctypes.c_void_p),
		("hStdOutput", ctypes.c_void_p),
		("hStdError", ctypes.c_void_p)
	]


class PROCESS_INFORMATION(ctypes.Structure):
	_fields_ = [
		("hProcess", ctypes.c_void_p),
		("hThread", ctypes.c_void_p),
		("dwProcessId", ctypes.c_uint32),
		("dwThreadId", ctypes.c_uint32)
	]


class WNDCLASS(ctypes.Structure):
	_fields_ = [
		("cbSize", ctypes.c_uint32),
		("style", ctypes.c_uint32),
		("lpfnWndProc", WNDPROC),
		("cbClsExtra", ctypes.c_int32),
		("cbWndExtra", ctypes.c_int32),
		("hInstance", ctypes.c_uint32),
		("hIcon", ctypes.c_uint32),
		("hIconSm", ctypes.c_uint32),
		("hCursor", ctypes.c_uint32),
		("hbrBackground", ctypes.c_uint32),
		("lpszMenuName", ctypes.c_char_p),
		("lpszClassName", ctypes.c_char_p)
	]


class POINT(ctypes.Structure):
	_fields_ = [
		("x", ctypes.c_int32),
		("y", ctypes.c_int32)
	]


class MSG(ctypes.Structure):
	_fields_ = [
		("hwnd", ctypes.c_void_p),
		("message", ctypes.c_uint32),
		("wParam", ctypes.c_uint32),
		("lParam", ctypes.c_int32),
		("time", ctypes.c_uint32),
		("pt", POINT)
	]


class COPYDATASTRUCT(ctypes.Structure):
	_fields_ = [
		("dwData", ctypes.c_uint32),
		("cbData", ctypes.c_uint32),
		("lpData", ctypes.c_void_p)
	]


def WndProc(hWnd, uMsg, wParam, lParam):
	global Hello, Sls, GameStr, Ticket, LastSvr, CharCnt, ClientTerminated, WebLinkUrl, cds, hWndProc, wParamProc

	std_out(uMsg)
	if uMsg == WM_COPYDATA:  # WM_COPYDATA
		pCds = ctypes.cast(lParam, ctypes.POINTER(COPYDATASTRUCT)).contents
		message = ctypes.cast(pCds.lpData, ctypes.c_char_p).value.decode('ascii')

		std_out(pCds, message)
		if message[-1] == '\0':
			message = message[:-1]

		cds = pCds
		hWndProc = hWnd
		wParamProc = wParam

		if message == "Hello!!":
			std_out(f"DLL: (WndProc) Hello")
			Hello = True
			return 1
		if message == "slsurl":
			std_out(f"DLL: (WndProc) slsurl")
			Sls = True
			return 1
		if message == "gamestr":
			std_out(f"DLL: (WndProc) gamestr")
			GameStr = True
			return 1
		if message.startswith("endPopup"):
			std_out(f"DLL: (WndProc) endPopup")
			EndPopup = int(message.split("(")[1].split(")")[0])
			if MessageListener is not None:
				MessageListener("endPopup", EndPopup)
			ctypes.windll.user32.PostQuitMessage(0)
			return 1
		if message.startswith("gameEvent"):
			std_out(f"DLL: (WndProc) gameEvent")
			GameEvent = int(message.split("(")[1].split(")")[0])
			if MessageListener is not None:
				MessageListener("gameEvent", GameEvent)
			return 1
		if message.startswith("getWebLinkUrl"):
			std_out(f"DLL: (WndProc) getWebLinkUrl")
			params = message.split("(")[1].split(")")[0].split(",")
			WebId = int(params[0])
			ServerId = int(params[1])
			CharacterId = int(params[2])
			if MessageListener is not None:
				MessageListener(message, WebId * 10000 + ServerId)
			return 1
		if MessageListener is not None:
			std_out(f"DLL: (WndProc) {message}")
			MessageListener(message, 0)
			return 1

	return ctypes.windll.user32.DefWindowProcW(hWnd, uMsg, wParam, lParam)


def MessageHandler():
	global Hello, Sls, GameStr, Ticket, LastSvr, CharCnt, WebLinkUrl

	while not ClientTerminated:
		if Hello:
			std_out(f"DLL: Hello")
			out = "Hello!!".encode()
			pCds = COPYDATASTRUCT()
			pCds.dwData = cds.dwData
			pCds.cbData = len(out) + 1
			pCds.lpData = ctypes.c_char_p(out)
			lpdwResult = ctypes.c_ulong()
			ctypes.windll.user32.SendMessageTimeoutA(
				wParamProc, WM_COPYDATA, hWndProc, ctypes.byref(pCds), 0x0, 0, ctypes.byref(lpdwResult)
			)
			Hello = False

		if Sls:
			std_out(f"DLL: Sls")
			pCds = COPYDATASTRUCT()
			pCds.dwData = cds.dwData
			pCds.cbData = len(SlsUrl) + 1
			pCds.lpData = ctypes.c_char_p(SlsUrl)
			lpdwResult = ctypes.c_ulong()
			ctypes.windll.user32.SendMessageTimeoutA(
				wParamProc, WM_COPYDATA, hWndProc, ctypes.byref(pCds), 0x0, 0, ctypes.byref(lpdwResult)
			)
			Sls = False

		if GameStr:
			std_out(f"DLL: GameStr")
			pCds = COPYDATASTRUCT()
			pCds.dwData = cds.dwData
			pCds.cbData = len(GameString) + 1
			pCds.lpData = ctypes.c_char_p(GameString)
			lpdwResult = ctypes.c_ulong()
			ctypes.windll.user32.SendMessageTimeoutA(
				wParamProc, WM_COPYDATA, hWndProc, ctypes.byref(pCds), 0x0, 0, ctypes.byref(lpdwResult)
			)
			GameStr = False

		if Ticket:
			std_out(f"DLL: Ticket")
			pCds = COPYDATASTRUCT()
			pCds.dwData = cds.dwData
			pCds.cbData = len(TicketStr) + 1
			pCds.lpData = ctypes.c_char_p(TicketStr)
			lpdwResult = ctypes.c_ulong()
			ctypes.windll.user32.SendMessageTimeoutA(
				wParamProc, WM_COPYDATA, hWndProc, ctypes.byref(pCds), 0x0, 0, ctypes.byref(lpdwResult)
			)
			Ticket = False

		if LastSvr:
			std_out(f"DLL: LastSvr")
			pCds = COPYDATASTRUCT()
			pCds.dwData = cds.dwData
			pCds.cbData = len(LastSvrStr) + 1
			pCds.lpData = ctypes.c_char_p(LastSvrStr)
			lpdwResult = ctypes.c_ulong()
			ctypes.windll.user32.SendMessageTimeoutA(
				wParamProc, WM_COPYDATA, hWndProc, ctypes.byref(pCds), 0x0, 0, ctypes.byref(lpdwResult)
			)
			LastSvr = False

		if CharCnt:
			std_out(f"DLL: CharCnt")
			pCds = COPYDATASTRUCT()
			pCds.dwData = cds.dwData
			pCds.cbData = len(CharCntStr) + 1
			pCds.lpData = ctypes.c_char_p(CharCntStr)
			lpdwResult = ctypes.c_ulong()
			ctypes.windll.user32.SendMessageTimeoutA(
				wParamProc, WM_COPYDATA, hWndProc, ctypes.byref(pCds), 0x0, 0, ctypes.byref(lpdwResult)
			)
			CharCnt = False

		if WebLinkUrl:
			std_out(f"DLL: WebLinkUrl")
			pCds = COPYDATASTRUCT()
			pCds.dwData = cds.dwData
			pCds.cbData = len(WebLinkUrlStr) + 1
			pCds.lpData = ctypes.c_char_p(WebLinkUrlStr)
			lpdwResult = ctypes.c_ulong()
			ctypes.windll.user32.SendMessageTimeoutA(
				wParamProc, WM_COPYDATA, hWndProc, ctypes.byref(pCds), 0x0, 0, ctypes.byref(lpdwResult)
			)
			WebLinkUrl = False

		time.sleep(1)

	return 1


def LaunchGame(lpSlsUrl, lpGameStr):
	global SlsUrl, GameString, Hello, Sls, GameStr, Ticket, LastSvr, CharCnt, ClientTerminated, TlExePath
	SlsUrl = lpSlsUrl
	GameString = lpGameStr
	TlExePath = "./TERA/TL.exe"
	Hello = False
	Sls = False
	GameStr = False
	ClientTerminated = False

	hModule = ctypes.windll.kernel32.GetModuleHandleW(None)

	windowClassEx = WNDCLASS()
	windowClassEx.cbSize = ctypes.sizeof(WNDCLASS)
	windowClassEx.lpszClassName = LAUNCHER_CLASS.encode()
	windowClassEx.hCursor = ctypes.windll.user32.LoadCursorW(None, IDC_ARROW)
	windowClassEx.hIcon = ctypes.windll.user32.LoadIconW(None, IDI_APPLICATION)
	windowClassEx.hIconSm = ctypes.windll.user32.LoadIconW(None, IDI_APPLICATION)
	windowClassEx.style = CS_HREDRAW | CS_VREDRAW
	windowClassEx.hbrBackground = 6
	windowClassEx.lpfnWndProc = WNDPROC(WndProc)
	windowClassEx.hInstance = hModule
	windowClassEx.cbClsExtra = 0
	windowClassEx.cbWndExtra = 0
	windowClassEx.lpszMenuName = None
	ctypes.windll.user32.RegisterClassExW(ctypes.byref(windowClassEx))

	wnd = ctypes.windll.user32.CreateWindowExA(
		WS_EX_APPWINDOW,
		windowClassEx.lpszClassName,
		b'???????d???!????????',
		0x00CF0000,
		-1,
		-1,
		-1,
		-1,
		None,
		None,
		hModule,
		None,
	)

	lpStartUpInfo = STARTUPINFO()
	lpStartUpInfo.cb = ctypes.sizeof(STARTUPINFO)
	lpProcessInformation = PROCESS_INFORMATION()

	if not ctypes.windll.kernel32.CreateProcessW(
			ctypes.c_wchar_p(TlExePath),
			None,
			None,
			None,
			True,
			4,
			None,
			None,
			ctypes.byref(lpStartUpInfo),
			ctypes.byref(lpProcessInformation),
	):
		message = f"Unable to start TL.exe. Error Code: {ctypes.windll.kernel32.GetLastError()}"
		ctypes.windll.user32.MessageBoxA(None, message, "TL.exe Error", MB_ICONERROR | MB_OK)
		return

	MessageHandlerFunc = ctypes.CFUNCTYPE(ctypes.c_uint)
	MessageHandlerPointer = MessageHandlerFunc(MessageHandler)

	ctypes.windll.kernel32.ResumeThread(lpProcessInformation.hThread)
	ctypes.windll.kernel32.CreateThread(0, 0, MessageHandlerPointer, None, 0, None)

	msg = MSG()
	while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), wnd, 0, 0, 1) > 0:
		std_out("MSG")
		ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
		ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

	std_out("Terminated")
	ClientTerminated = True
	ctypes.windll.kernel32.CloseHandle(lpProcessInformation.hProcess)


def RegisterMessageListener(f):
	std_out(f"DLL: Registered Message Listener")
	global MessageListener
	MessageListener = f


def SendMessageToClient(responseTo, message):
	std_out(f"DLL: {responseTo} | {message}")
	global TicketStr, LastSvrStr, CharCntStr, WebLinkUrlStr, Ticket, LastSvr, CharCnt, WebLinkUrl

	if responseTo == "ticket":
		TicketStr = message
		Ticket = True
	elif responseTo == "last_svr":
		LastSvrStr = message
		LastSvr = True
	elif responseTo == "char_cnt":
		CharCntStr = message
		CharCnt = True
	elif responseTo == "getWebLinkUrl":
		WebLinkUrlStr = message
		WebLinkUrl = True
