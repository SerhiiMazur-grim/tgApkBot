from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats, BotCommandScopeChat

from config.settings import Settings


async def set_commands(bot: Bot, settings: Settings) -> None:
    admin_id: int = settings.admin_chat_id
    
    all_private_chats_commands = [
        BotCommand(command='start',
                   description='–  Start dialog with bot'),
        BotCommand(command='language',
                   description='–  Change the language'),
    ]
    admin_commands = [
        BotCommand(command='image_id',
                   description='–  Get the image ID'),
        BotCommand(command='add_image_to_galery',
                   description='–  Add images to galery'),
        BotCommand(command='add_sub_channel',
                   description='–  Add channel for subscibe'),
        BotCommand(command='all_sub_channel',
                   description='–  Show all channels for subscibe'),
        BotCommand(command='delete_sub_channel',
                   description='–  Delete channel for subscibe'),
        BotCommand(command='add_ref_start',
                   description='–  Add greetings for referral url'),
        BotCommand(command='delete_ref_start',
                   description='–  Delete greetings for referral url'),
        BotCommand(command='upload_apk1',
                   description='–  Upload APK1'),
        BotCommand(command='upload_apk2',
                   description='–  Upload APK2'),
        BotCommand(command='update_apk',
                   description='–  Update APK'),
        BotCommand(command='send_post_to_all',
                   description='–  Send your post to all users'),
    ]
    
    admin_commands = all_private_chats_commands + admin_commands
    
    await bot.set_my_commands(commands=all_private_chats_commands,
                              scope=BotCommandScopeAllPrivateChats())
    await bot.set_my_commands(commands=admin_commands,
                              scope=BotCommandScopeChat(chat_id=admin_id))
