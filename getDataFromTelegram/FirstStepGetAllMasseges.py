'''
 This module make

Athor: Gansior Alexander, gansior@gansior.ru, +79173383804
Starting 2022/02/04
Ending 2022//
    
'''

from cgitb import text
import json
import os
from collections import Counter
from pprint import pprint
# для корректного переноса времени сообщений в json
from datetime import date, datetime

# класс для создания соединения с Telegram
from telethon import TelegramClient, events, sync

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest


def get_config(name_file: str):
    with open(name_file) as f:
        d = json.load(f)
        return d['api_id'], d['api_hash'], d['username'], d['api_id']


def get_all_users_chanel(name_chanel_loc: str):
    """get config connection with Telegram

    Args:
        name_chanel_loc (str): [description]
    """

    cwd = os.getcwd()
    work_dir = cwd.split('ETL_sistems')
    name = f'{work_dir[0]}ETL_sistems/config/telegram.json'
    api_id, api_hash, username, phone = get_config(name)
    print(api_id, api_hash, username, phone)

    client = TelegramClient(username, api_id, api_hash)
    client.start()

    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

    # Work with channel name_chanel_loc
    user_input_channel = name_chanel_loc

    # get all users of chanel
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = client.get_entity(entity)
    offset = 0
    limit_users = 100
    all_participants = []
    data_text = str(datetime.now()).replace(
        '-', '_').replace(' ', '_').replace(':', '_').replace('.', '_')
    name_file_user = f'{work_dir[0]}ETL_sistems/datasets_com/AGI/' + \
        name_chanel_loc.split('/')[-1] + '_' + data_text + '_User.txt'
    data_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    while True:
        participants = client(GetParticipantsRequest(
            my_channel, ChannelParticipantsSearch(''), offset, limit_users,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
    print(f'KOl users = {offset}')
    with open(name_file_user, 'a', encoding='utf8') as outfile:
        outfile.write("id^first_name^last_name^user^phone^is_bot^data\n")
        for participant in all_participants:
            name = ''
            last_name = ''
            if isinstance(participant.first_name, str):
                name = f'{participant.first_name}'
            if isinstance(participant.last_name, str):
                last_name = f'{participant.last_name}'
            # print(name, last_name, sep= ' ------- ')
            outfile.write(
                f"{participant.id}^{name}^{last_name}^{participant.username}^"
                f"{participant.phone}^{participant.bot}^{data_now}\n")
    client.disconnect()


def get_info_chanel(name_chanel: str):

    # get config connection with Telegram
    cwd = os.getcwd()
    work_dir = cwd.split('ETL_sistems')
    name = f'{work_dir[0]}/ETL_sistems/config/telegram.json'
    api_id, api_hash, username, phone = get_config(name)
    print(api_id, api_hash, username, phone)

    client = TelegramClient(username, api_id, api_hash)
    client.start()

    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))

    # Work with channel name_chanel
    user_input_channel = name_chanel

    # get all users of chanel
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = client.get_entity(entity)

    # offset = 0
    # limit_users = 100
    # all_participants = []
    name_file_user = f'{work_dir[0]}ETL_sistems/datasets_com/AGI/' + \
        name_chanel.split('/')[-1] + '_User.txt'
    nameFileMes = f'{work_dir[0]}ETL_sistems/datasets_com/AGI/' + \
        name_chanel.split('/')[-1] + '_Mes.txt'
    # print(name_file_user, nameFileMes, sep = ' --- ')
    # while True:
    #     participants = client(GetParticipantsRequest(
    #         my_channel, ChannelParticipantsSearch(''), offset, limit_users,
    #         hash=0
    #     ))
    #     if not participants.users:
    #         break
    #     all_participants.extend(participants.users)
    #     offset += len(participants.users)
    # print(f'KOl users = {offset}')
    # with open(name_file_user , 'w', encoding='utf8') as outfile:
    #     outfile.write("id^first_name^last_name^user^phone^is_bot\n")
    #     for participant in all_participants:
    #         name = ''
    #         last_name = ''
    #         if type(participant.first_name) == str : name = u'{}'.format(participant.first_name)
    #         if type(participant.last_name) == str : last_name = u'{}'.format(participant.last_name)
    #         #print(name, last_name, sep= ' ------- ')
    #         outfile.write(f"{participant.id}^{name}^{last_name}^{participant.username}^{participant.phone}^{participant.bot}\n")

    # get all messages of chanel
    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0
    k = 0
    while True:
        # print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        with open(nameFileMes, 'a') as ff:
            for message in messages:
                ff.write("<============================>\n")
                mmrez = message.to_dict()
                for mm in mmrez:
                    ff.write(f"{mm} : {mmrez[mm]}\n")
                k += 1
        offset_id = messages[len(messages) - 1].id
        # print('k == ', k)
    print('com Messeges {nameFileMes}k == ', k)
    client.disconnect()


if __name__ == '__main__':
    listName = [
        'https://t.me/agiethics',
        'https://t.me/agitopics/22606',
        # 'https://t.me/ai_life',
        # 'https://t.me/agirussia',
        # 'https://t.me/AGIRussia_SCA',
        # 'https://t.me/OpenTalksAI',
        # 'https://t.me/agirussianews'
        ]
    for name_chanel in listName:
        # get_all_users_chanel(name_chanel)
        get_info_chanel(name_chanel)
