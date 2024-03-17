import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest

api_ids = ['27789865', '22409815', '29074750']
api_hashes = ['a596f5e0a8a573d7dda26638effe3d08', 'dc41b7b3df7d42d8300fe5f408abb1d8', '37a7ca04d2a088e8c48b6248a6beaf76']
phone_numbers = ['+5562998225591', '+5562986356665', '+17542598817']

group_username = 'https://t.me/pato_teste' # Substitua pelo nome de usuário ou ID do seu grupo

clients = []

for i in range(len(phone_numbers)):
    api_id = int(api_ids[i])
    api_hash = api_hashes[i]
    phone_number = phone_numbers[i]

    client = TelegramClient(phone_number, api_id, api_hash)
    client.start()
    clients.append(client)

print("Clients: ", clients)

async def join_group(client):
    try:
        await client(JoinChannelRequest(group_username))
        print(f'{client.session.auth_key} entrou no grupo {group_username}')
    except Exception as e:
        print(f'Erro ao entrar no grupo: {str(e)}')

for client in clients:
    asyncio.get_event_loop().run_until_complete(join_group(client))