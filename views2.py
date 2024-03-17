from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetPeerDialogsRequest
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

api_id = 'your_api_id'
api_hash = 'your_api_hash'
phone_number = '+17542598817'
group_username = 'https://t.me/pato_teste'
message_to_view = 'Hello, world!'

with TelegramClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(send_views(group_username, message_to_view))

async def send_views(group_username, message_to_view):
    await client.send_message(group_username, message_to_view)

    # This method retrieves all the dialogs of the current user.
    dialogs = await client(GetPeerDialogsRequest())

    for dialog in dialogs.dialogs:
        # We check if the dialog is related to the group
        if dialog.peer.username == group_username:
            # If so, we send a view action to the last message
            await client(SendMessageRequest(
                peer=dialog.peer,
                message='',
                reply_to_msg_id=dialog.top_message,
                action=GetPeerDialogsRequest.GetPeerDialogsRequest()
            ))