
# TERA Launcher

This project is a pure Python implementation to launch the MMORPG "TERA Online." It leverages Windows APIs to initiate the game client launcher (`TL.exe`) and handle in-game events, connection, and exit statuses.

## Features

- **Game Launcher**: Starts the TERA Online client launcher (`TL.exe`) and initializes necessary settings to play the game.
- **Message Listener**: Registers and listens for game-related events, exit codes, and error messages.
- **Event Logging**: Logs game events, errors, and status codes with custom mapping for easy debugging.
- **Server Communication**: Manages server-related messages, such as last server, character count, and web link URLs.
- **Verbose Error Handling**: Provides detailed error messages for game crashes, network errors, and authentication issues.

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

1. **Set Game Config**: Set up the game configuration data
   ```python
   from TeraLauncher import GameConfig
   
   game_config = GameConfig()
   
   # Choose language code to load according datacenter
   # en: USA, fr: FRA, kr: KOR, de: GER, uk: EUR, ru: RUS, jp: JPN, tw: TW, th: THA
   game_config.lang = SESSION['lang_code'],
   
   # URL to your API server: string
   game_config.url = f"{SERVER_HOST}",
   game_config.sls = f"/path/to/server_list.{game_config.lang}"
   
   # User auth token: string
   game_config.ticket = SESSION['auth_key']
   game_config.token = SESSION['auth_key']
   game_config.auth_token = SESSION['auth_key']
   game_config.access_token = SESSION['auth_key']
   
   # User name: string
   game_config.account_name = SESSION['user_name']
   game_config.game_account_name = SESSION['user_name']
   game_config.master_account_name = SESSION['user_name']
   
   # User ID: integer
   game_config.id = SESSION['user_id']
   game_config.user_id = SESSION['user_id']
   
   # User access permissions: integer
   game_config.access_level = SESSION['access_level']
   game_config.user_permission = SESSION['user_permission']
   ```
       
2. **Initialize IPC Loader**: 
   Create a new `IPCLoader` object by passing game configuration data.
   ```python
   from TeraLauncher import IPCLoader
   
   # Initialize the IPC Loader class
   TL = IPCLoader(game_config, exit_callback, logger, debug)
   TL.MessageListener(b"gameEvent", 1000)
   ```

3. **Register Message Listener**:
   Set up a listener to handle server and game messages.

    ```python
    # Message Listener
    mlThread = Thread(target=TL.RegisterMessageListener, daemon=True)
    mlThread.start()
    TID_ML = mlThread.native_id
    ```

4. **Launch Game**:
   Call `LaunchGame()` on the `Loader` instance to start the TERA client.

    ```python
    # Game Client
    mainThread = Thread(target=TL.LaunchGame, daemon=True)
    mainThread.start()
    TID_TERA = mainThread.native_id
    ```

## Event Codes and Error Handling

Game events and error messages are logged with specific codes and descriptions:
- **Exit Codes**: Defined in `CLIENT_END_CODE`, such as `5` for graphics driver errors and `10` for insufficient RAM.
- **Launcher Events**: Defined in `LAUNCHER_EVENT_CODE`, including authentication, patcher, and GUI initialization events.

## Contributing

1. Fork the repository.
2. Create a new feature branch.
3. Commit your changes and submit a pull request.

## License

This project is licensed under the MIT License.
