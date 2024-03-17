from telethon.sync import TelegramClient, events
from telethon.tl import types
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import SendReactionRequest, SendMessageRequest

api_ids = ['27789865', '22409815', '29074750']
api_hashes = ['a596f5e0a8a573d7dda26638effe3d08', 'dc41b7b3df7d42d8300fe5f408abb1d8',
              '37a7ca04d2a088e8c48b6248a6beaf76']
phone_numbers = ['+5562998225591', '+5562986356665', '+17542598817']

group_username = 'https://t.me/BRABOR10'  # Substitua pelo username ou ID do seu grupo

clients = []


# Função para reagir a mensagens
def react_to_messages(client, num_messages=3):
    chat_id = client.get_entity(group_username)  # Obtenha o chat_id do grupo
    messages = client.get_messages(chat_id, limit=num_messages)  # Obtenha as mensagens

    for message in messages:
        try:
            # Reaja à mensagem
            client(SendReactionRequest(
                peer=chat_id,
                msg_id=message.id,
                reaction=[types.ReactionEmoji(
                    emoticon='❤️'
                )]
            ))
            print(f'Reagiu à mensagem {message.id}')
        except Exception as e:
            print(f"Erro ao processar mensagem {message.id}: {e}")


# Função para aderir ao grupo
def join_group(client):
    client(JoinChannelRequest(group_username))


# Função para notificar quem reagiu
async def notify_reactions(client, event):
    chat_id = client.get_entity(group_username)
    message = event.message
    reactions = await client.get_reactions(chat_id, message, "❤️")  # Obtenha quem reagiu com ❤️

    if reactions:
        user_mentions = ", ".join([f"@{reaction.sender.username}" for reaction in reactions])
        notify_message = f"👍 Reações a esta mensagem por: {user_mentions}"
        await client(SendMessageRequest(chat_id, notify_message, reply_to=message.id))


# Criar e iniciar os clientes do Telegram com bancos de dados diferentes
for i in range(len(phone_numbers)):
    api_id = int(api_ids[i])
    api_hash = api_hashes[i]
    phone_number = phone_numbers[i]

    # Use um banco de dados SQLite diferente para cada cliente
    client = TelegramClient(f'session_{i}', api_id, api_hash)
    client.start(phone_number)
    clients.append(client)
    join_group(client)  # Junte-se ao grupo ao criar o cliente

print("Clientes: ", clients)


# Manipulador de eventos para lidar com novas mensagens
async def handle_new_message(event):
    try:
        for client in clients:
            # Reaja à nova mensagem em todos os clientes
            await client(SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.id,
                reaction=[types.ReactionEmoji(
                    emoticon='👍'
                )]
            ))
            print(f'Reagiu à nova mensagem {event.id}')

        # Notificar quem reagiu
        await notify_reactions(clients[0], event)  # Notificar apenas a partir do primeiro cliente

    except Exception as e:
        print(f"Erro ao processar nova mensagem {event.id}: {e}")


# Adicione o manipulador de eventos para todos os clientes
for client in clients:
    client.add_event_handler(handle_new_message, events.NewMessage(chats=group_username, incoming=True))

# Executar os clientes para começar a ouvir eventos
for client in clients:
    client.run_until_disconnected()
