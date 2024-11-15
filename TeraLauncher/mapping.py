CLIENT_END_CODE = {
    0: {
        0: 'Standard exit of the the game. Normal close.'
    },
	1: {
		0: 'Error initializing anti cheat service. Cannot start client.'
	},
	3: {
		0: 'Error in authentication string. Cannot start client.'
	},
    5: {
        0: 'Graphics driver error, please check your graphics card settings and make sure it has the latest driver.'
    },
    6: {
        0: 'Error reading data file. Please perform an integrity check.'
    },
    7: {
        0: 'Standard exit of the the game. Application close.'
    },
    8: {
        0: 'An internet connection error resulted in the game being quit. Please check your internet access.'
    },
    9: {
        0: 'Failed to get authentication information. Please check your internet access.'
    },
    10: {
        0: 'There is not enough RAM, try the following measures: 1. Close other programs; 2. Check all files; 3. Set graphics settings to minimum. '
    },
    11: {
        0: 'Failed to initialize the video card. Make sure you have DirectX 9c 32-bit or higher installed and an updated video driver.'
    },
    12: {
        0: 'Sorry, but your graphics card does not support this game.'
    },
    15: {
        0: 'Since you have not been active for a long time, the game was automatically closed.'
    },
    16: {
        0: 'Standard exit of the the game. Quick close.'
    },
    30: {
        0: 'You have been disconnected from the TERA world!'
    },
    31: {
        0: 'You have been <strong>kicked</strong> from the TERA world! For further questions, <a href="/support" target="_blank">contact support</a>!'
    },
    32: {
        0: 'You have been <strong>banned</strong> from the TERA world! For further questions, <a href="/support" target="_blank">contact support</a>!'
    },
    33: {
        0: 'The administrator has disconnected you from the TERA world!'
    },
    34: {
        0: 'The administrator disconnected you from the game.'
    },
    35: {
        0: 'You have been disconnected you from the game.'
    },
    257: {
        0: 'Login failed, please try login again later.',
        13: 'This account has been banned.',
        32781: 'Your account has been banned, for all questions please contact support.',
        50099: 'Network Error. Please check your internet connection.'
    },
    258: {
        0: 'Payment system error.'
    },
    259: {
        0: 'An attempt was made to enter the game with a different device using this account. Please make sure that your username and password are safe. If it was not you, we recommend that you urgently contact the user support service.'
    },
    260: {
        0: 'Unable to get the list of servers, please try again later:0',
        404: 'Unable to get the list of servers, possibly a problem with your internet connection:404.'
    },
    261: {
        0: 'Login failed, please try again later:261.'
    },
    262: {
        0: 'The account is currently being used from another device. Please make sure that your username and password are safe. If this is not you, we recommend that you urgently contact the user support service.'
    },
    265: {
        0: 'Some client files are missing or damaged. Please run a file check.'
    },
    273: {
        0: 'Server list is currently not available, please try again later.',
        3: 'Your internet connection is unstable, please check your internet connection and try again.',
    },
    274: {
        0: 'Error loading settings file. Please make sure your internet connection is stable and try again.'
    },
    275: {
        0: "The game's graphics settings are too high, please set a lower graphics setting.<br><br>Make sure you have the latest graphics card driver installed.",
        2: 'Base files for <strong>{app}</strong> not found.<br><br>Check our <a href="https://exval.network/support" target="_blank">support center</a> a possible solution and fix.',
        5: 'File access to <strong>{app}</strong> banned.<br><br>Check our <a href="https://exval.network/support" target="_blank">support center</a> for possible solutions.',
        193: 'Executable for <strong>{app}</strong> is not a Win32 application.<br><br>Check our <a href="https://exval.network/support" target="_blank">support center</a> for possible solutions.',
        216: 'The <strong>{app}</strong> is not compatible with the version of Windows you are using.<br><br>Check our <a href="https://exval.network/support" target="_blank">support center</a> for possible solutions.',
        740: 'Insufficient permission to run <strong>{app}</strong>.<br><br>Start the launcher as an administrator. Rightclick on the launcher, select "Run as administrator".',
        1392: 'Files for <strong>{app}</strong> damaged or no access to read it.<br><br>Use the file checker on the bottom left menu, to check and repair the game files.',
    },
    276: {
        0: 'Failed to update the launcher. Please make sure your internet connection is stable and try again.'
    },
    277: {
        0: 'Patch file format error. Please make sure your internet connection is stable and try again.'
    },
    278: {
        0: 'The program files are damaged. Please check the files with the launcher and restore the game files.'
    },
    1337: {
        0: 'Garbage can detected! Please check Layer 8 and try again. If the problem persists, please check our <a href="https://exval.network/support" target="_blank">support center</a>.'
    },
    32768: {
        0: 'The server is undergoing technical work. You can find out about the time of completion of work on the official website. '
    },
    32769: {
        0: 'The first closed TERA testing has been completed. Please continue to follow TERA news!'
    },
    32770: {
        0: 'The server is temporarily unavailable due to technical work. Please follow the news on the official website..'
    },
    65280: {
        0: 'An error occurred during the game and the client was closed. We recommend that you conduct a full scan of the game files'
    },
    65535: {
        0: 'System crash of the game. Please check the files using the launcher. If the problem persists, please contact support. '
    }
}

LAUNCHER_EVENT_CODE = {
    0: "GL_EVENT_LAUNCHER_START",
    1: "GL_EVENT_LAUNCHER_END",
    2: "GL_EVENT_MANIFEST_READ_LOCAL",
    3: "GL_EVENT_MANIFEST_READ_WEB",
    4: "GL_EVENT_MANIFEST_READ_ERROR",
    5: "GL_EVENT_MANIFEST_WRITE",
    6: "GL_EVENT_MANIFEST_COMPARE",
    7: "GL_EVENT_MANIFEST_GATHER",
    8: "GL_EVENT_MANIFEST_HASHING",
    9: "GL_EVENT_MANIFEST_HASHING_ERROR",
    10: "GL_EVENT_DOWNLOAD_START",
    11: "GL_EVENT_DOWNLOAD_END",
    12: "GL_EVENT_DOWNLOAD_ERROR",
    13: "GL_EVENT_DOWNLOAD",
    20: "GL_EVENT_CONFIG_READ",
    21: "GL_EVENT_CONFIG_SAVE",
    22: "GL_EVENT_CONFIG_ERROR",
    30: "GL_EVENT_MISSING_DLL",
    31: "GL_EVENT_MISSING_INI",
    32: "GL_EVENT_MISSING_ETC",
    40: "GL_EVENT_LOGIN_START",
    41: "GL_EVENT_LOGIN_OK",
    42: "GL_EVENT_LOGIN_ERROR",
    50: "GL_EVENT_CONSOLE_START",
    51: "GL_EVENT_CONSOLE_OK",
    52: "GL_EVENT_CONSOLE_ERROR",
    60: "GL_EVENT_GUI_START",
    61: "GL_EVENT_GUI_OK",
    62: "GL_EVENT_GUI_ERROR",
    70: "GL_EVENT_PATCHER_START",
    71: "GL_EVENT_PATCHER_OK",
    72: "GL_EVENT_PATCHER_ERROR",
    100: "GL_EVENT_ARGON_INIT",
    101: "GL_EVENT_ARGON_INIT_OK",
    102: "GL_EVENT_ARGON_INIT_ERROR",
    103: "GL_EVENT_ARGON_CONN",
    104: "GL_EVENT_ARGON_CONN_OK",
    105: "GL_EVENT_ARGON_CONN_ERROR",
    106: "GL_EVENT_ARGON_CFG",
    107: "GL_EVENT_ARGON_CFG_OK",
    108: "GL_EVENT_ARGON_CFG_ERROR",
    109: "GL_EVENT_ARGON_USER",
    110: "GL_EVENT_ARGON_USER_OK",
    111: "GL_EVENT_ARGON_USER_ERROR",
    112: "GL_EVENT_ARGON_ROUTE",
    113: "GL_EVENT_ARGON_ROUTE_OK",
    114: "GL_EVENT_ARGON_ROUTE_ERROR",
    115: "GL_EVENT_ARGON_HWID",
    116: "GL_EVENT_ARGON_HWID_OK",
    117: "GL_EVENT_ARGON_HWID_ERROR",
    999: "GL_EVENT_CLIENT_ERROR",
    1000: "GL_EVENT_CLIENT_START",
    1001: "GL_EVENT_CLIENT_END",
    1002: "GL_EVENT_SERVER_SELECT",
    1003: "GL_EVENT_SERVER_TO_LOBBY",
    1004: "GL_EVENT_LOBBY_LOAD_COMPLETE",
    1005: "GL_EVENT_LOBBY_TO_CREATE",
    1006: "GL_EVENT_LOBBY_TO_SERVER",
    1007: "GL_EVENT_DELETE_CHAR",
    1008: "GL_EVENT_CREATE_TO_LOBBY",
    1009: "GL_EVENT_CREATE_LOAD_COMPLETE",
    1010: "GL_EVENT_CREATE_CHAR_OK",
    1011: "GL_EVENT_ENTER_WORLD",
    1012: "GL_EVENT_ENTER_WORLD_OK",
    1013: "GL_EVENT_WORLD_TO_LOBBY",
    1014: "GL_EVENT_GET_ON_PEGASUS",
    1015: "GL_EVENT_GET_OFF_PEGASUS",
    1016: "GL_EVENT_MOVE_CHANNEL",
    1017: "GL_EVENT_MOVE_CHANNEL_OK",
    1018: "GL_EVENT_ESCAPE",
    1019: "GL_EVENT_ESCAPE_OK",
    2000: "GL_EVENT_CLIENT_START",
    2001: "GL_EVENT_CLIENT_END",
    2002: "GL_EVENT_CLIENT_AUTH",
    2003: "GL_EVENT_CLIENT_OK",
    9000: "GL_EVENT_UNKNOWN_CODE",
}
