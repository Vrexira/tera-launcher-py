
# TERA Launcher

This project is a pure Python implementation to launch the MMORPG "TERA Online." It leverages Windows APIs to initiate the game client launcher (`TL.exe`) and handle in-game events, connection, and exit statuses. This project uses 32-bit Python due to compatibility requirements with TERA's client launcher (`TL.exe`).

## Features

- **Game Launcher**: Starts the TERA Online client launcher (`TL.exe`) and initializes necessary settings to play the game.
- **Message Listener**: Registers and listens for game-related events, exit codes, and error messages.
- **Event Logging**: Logs game events, errors, and status codes with custom mapping for easy debugging.
- **Server Communication**: Manages server-related messages, such as last server, character count, and web link URLs.
- **Custom Error Handling**: Provides detailed error messages for game crashes, network errors, and authentication issues.

## Project Structure

- `DynamicLinkLibrary.py`: Defines core ctypes structures, message handling functions, and game-launching routines.
- `Helper.py`: Includes helper functions for logging (`std_out`).
- `Mapping.py`: Maps exit codes and launcher event codes to descriptive error messages.
- `TeraLoader.py`: Primary interface class for launching and controlling the game client.

## Requirements

- Python (32-bit)
- `pywin32==306` for Windows-specific APIs
- `ctypes` (standard library)

To install `pywin32`, run:
```bash
pip install pywin32==306
```

## Usage

1. **Initialize Loader**:
   Create a new `Loader` object by passing game configuration data.

    ```python
    from TeraLoader import Loader
    
    # Example Game String of all possible keys and their intended values
    game_str = {
        "url": f"{SERVER_HOST}",
        "sls": f"/rest/v1/launcherApi/GetServerList.{lang_code}",
        "lang": f"{lang_code}",
        "ticket": f"{SESSION['authKey']}",
        "token": f"{SESSION['authKey']}",
        "auth_token": f"{SESSION['authKey']}",
        "access_token": f"{SESSION['authKey']}",
        "last_connected_server_id": SESSION['lastServer'],
        "account_name": "TERA",
        "account_status": 1,
        "game_account_name": "TERA",
        "master_account_name": f"{SESSION['accountDBID']}",
        "chars_per_server": [
            {"id": "2800", "char_count": "10"},
            {"id": "2801", "char_count": "11"}
        ],
        "id": SESSION['accountDBID'],
        "user_id": SESSION['accountDBID'],
        "last_svr": SESSION['lastServer'],
        "char_cnt": 10,
        "access_level": SESSION['privilege'],
        "user_permission": SESSION['permission'],
        "result-code": 200,
        "result-message": "OK"
    }

    def exit_callback():
        print("Game exited")

    TL = Loader(game_str, exit_callback, debug=True)

    # message listener
    TL.MessageListener(b"gameEvent", 1000)
    
    ```

2. **Register Message Listener**:
   Set up a listener to handle server and game messages.

    ```python
    # Message Listener
    mlThread = Thread(target=TL.RegisterMessageListener, daemon=True)
    mlThread.start()
    TID_ML = mlThread.native_id
    if DEBUG: std_out(f"Registered Message Listener | TID: {TID_ML}")
    ```

3. **Launch Game**:
   Call `LaunchGame()` on the `Loader` instance to start the TERA client.

    ```python
    # Game Client
    mainThread = Thread(target=TL.LaunchGame, daemon=True)
    mainThread.start()
    TID_TERA = mainThread.native_id
    if DEBUG: std_out(f"Launching TERA Game Client | TID: {TID_TERA}")
    ```

## Event Codes and Error Handling

Game events and error messages are logged with specific codes and descriptions:
- **Exit Codes**: Defined in `CLIENT_END_CODE`, such as `5` for graphics driver errors and `10` for insufficient RAM.
- **Launcher Events**: Defined in `LAUNCHER_EVENT_CODE`, including authentication, patcher, and GUI initialization events.

## Debugging and Logs

All messages and codes are logged via the `std_out` function in `Helper.py`, providing insights into game events and errors. Set `debug=True` when initializing the `Loader` to enable detailed output.

## Contributing

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes and submit a pull request.

## License

This project is licensed under the MIT License.
