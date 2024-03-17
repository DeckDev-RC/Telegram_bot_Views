from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, MarkDialogUnreadRequest
from telethon.tl.types import InputPeerEmpty, InputDialogPeer
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
import asyncio

api_ids = ['27789865', '22409815', '29074750']
api_hashes = ['a596f5e0a8a573d7dda26638effe3d08', 'dc41b7b3df7d42d8300fe5f408abb1d8', '37a7ca04d2a088e8c48b6248a6beaf76']
phone_numbers = ['+5562998225591', '+5562986356665', '+17542598817']

group_username = 'https://t.me/pato_teste'  # Nome de usuário do grupo

clients = []

for i in range(len(api_ids)):
    client = TelegramClient(f'session_{i}', api_ids[i], api_hashes[i])
    clients.append((client, phone_numbers[i]))

async def main(client, phone_number):
    try:
        await client.send_message('me', 'Teste de conexão com a API do Telegram.')
    except PeerFloodError:
        print(f'Esperando para {phone_number}...')
        await asyncio.sleep(60)
        await main(client, phone_number)
    except UserPrivacyRestrictedError:
        print(f'Conta de {phone_number} bloqueada, não é possível continuar.')
        return
    dialogs = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))
    dialog_count = len(dialogs.dialogs)
    for i in range(0, dialog_count):
        await asyncio.sleep(1)
        try:
            dialog = dialogs.dialogs[i]
            entity = await client.get_entity(dialog.peer)
            if entity.username == group_username:
                print(f'Enviando views para a conversa em {phone_number}: {entity.title}')
                await client(MarkDialogUnreadRequest(
                    peer=InputDialogPeer(
                        peer=entity,
                        is_message=False
                    ),
                    is_marked_as_unread=False
                ))
        except PeerFloodError:
            print(f'Esperando para {phone_number}...')
            await asyncio.sleep(60)
            entity = await client.get_entity(dialog.peer)
            await client(MarkDialogUnreadRequest(
                peer=InputDialogPeer(
                    peer=entity,
                    is_message=False
                ),
                is_marked_as_unread=False
            ))

for client, phone_number in clients:
    print(f'Executando cliente para {phone_number}')
    with client:
        client.loop.run_until_complete(main(client, phone_number))
