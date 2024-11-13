from dataclasses import dataclass, field
from typing import List


@dataclass
class ServerCharacters:
    id: str
    char_count: str


@dataclass
class GameConfig:
    url: str = "<server_host>"
    sls: str = "<path_to_server_list>"
    lang: str = "<lang_code>"
    ticket: str = "<auth_key>"
    token: str = "<auth_key>"
    auth_token: str = "<auth_key>"
    access_token: str = "<auth_key>"
    account_name: str = "<user_name>"
    account_status: int = 1
    game_account_name: str = "<user_name>"
    master_account_name: str = "<user_name>"
    last_connected_server_id: int = 2800  # server_id
    chars_per_server: List[ServerCharacters] = field(
        default_factory = lambda: [ServerCharacters(id = "2800", char_count = "1").__dict__]
    )
    id: int = 0  # user_id
    user_id: int = 0  # user_id
    last_svr: int = 2800  # server_id
    char_cnt: int = 1
    access_level: int = 0
    user_permission: int = 0
