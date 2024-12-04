from aiogram.types import Message
from aiogram.types.input_media_animation import InputMediaAnimation
from aiogram.types.input_media_document import InputMediaDocument
from aiogram.types.input_media_audio import InputMediaAudio
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.types.input_media_video import InputMediaVideo


async def get_media_group_list(data: list) -> list:
    post: Message
    media_list = []
    for post in data:
        if post.photo:
            media = post.photo[-1].file_id
            caption = post.caption
            caption_entities = post.caption_entities
            photo = InputMediaPhoto(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(photo)
            continue
        
        elif post.video:
            media = post.video.file_id
            caption = post.caption
            caption_entities = post.caption_entities
            video = InputMediaVideo(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(video)
            continue
        
        elif post.animation:
            media = post.animation.file_id
            caption = post.caption
            caption_entities = post.caption_entities           
            animation = InputMediaAnimation(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(animation)
            continue

        elif post.document:
            media = post.document.file_id
            caption = post.caption
            caption_entities = post.caption_entities
            document = InputMediaDocument(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(document)
            continue

        elif post.audio:
            media = post.audio.file_id
            caption = post.caption
            caption_entities = post.caption_entities
            audio = InputMediaAudio(media=media, caption=caption, caption_entities=caption_entities)
            media_list.append(audio)
            continue
    return media_list
