import sys
import threading

from TeraLauncher import IPCLoader, GameConfig, CLIENT_END_CODE


def exit_callback():
    print("Game exited")
    sys.exit(0)

def run():
    game_config = GameConfig()
    
    # Choose language code to load according datacenter
    # en: USA, fr: FRA, kr: KOR, de: GER, uk: EUR, ru: RUS, jp: JPN, tw: TW, th: THA
    game_config.lang = SESSION['lang_code'],
    
    game_config.url = f"{SERVER_HOST}",
    game_config.sls = f"/rest/v1/launcherApi/GetServerList.{game_config.lang}"
    
    game_config.ticket = SESSION['auth_key']
    game_config.token = SESSION['auth_key']
    game_config.auth_token = SESSION['auth_key']
    game_config.access_token = SESSION['auth_key']
    
    game_config.account_name = SESSION['user_name']
    game_config.game_account_name = SESSION['user_name']
    game_config.master_account_name = SESSION['user_name']
    
    game_config.id = SESSION['user_id']
    game_config.user_id = SESSION['user_id']
    
    game_config.access_level = SESSION.get('access_level', 0)
    game_config.user_permission = SESSION.get('user_permission', 0)
    
    debug = True
    
    # Initialize the IPC Loader class
    GL = IPCLoader(game_config, exit_callback, logger, debug)
    GL.MessageListener(b"gameEvent", 1000)
    
    # Message Listener
    mlThread = threading.Thread(target = GL.RegisterMessageListener, daemon = True)
    mlThread.start()
    logger.info(f"Started IPC Message Listener")
    
    # Launch TERA
    status = GL.LaunchGame()
    if status == 0:
        err = False
        logger.info("Ending application")
    elif status in CLIENT_END_CODE:
        err = CLIENT_END_CODE[status][0]
    else:
        err = status
    
    return err
