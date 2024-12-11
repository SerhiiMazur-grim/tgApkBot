from config.settings import Settings


SETTINGS: Settings = Settings()


def is_admin(user_id: int | str) -> bool:
    user_id = int(user_id)
    
    if user_id in SETTINGS.admin_chat_id:
        return True
    return False
