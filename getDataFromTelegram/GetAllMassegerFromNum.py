'''
 This module make

Athor: Gansior Alexander, gansior@gansior.ru, +79173383804
Starting 2022/07/24
Ending 2022//

'''
import json
import os
import csv
from pprint import pprint
import asyncio
from time import sleep
# класс для создания соединения с Telegram
from telethon import TelegramClient
# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import PeerChannel

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest


# loop = asyncio.get_event_loop()

def get_config(name_file: str):
    """AI is creating summary for get_config

    Args:
        name_file (str): [description]

    Returns:
        [type]: [description]
    """
    with open(name_file, encoding='utf 8') as f:
        d = json.load(f)
        return d['api_id'], d['api_hash'], d['username'], d['api_id']


async def get_info_chanel_num(name_chanel_loc: list):
    """AI is creating summary for getInfoChanelNum

    Args:
        name_chanel_loc (list): [description]
    """
    print(name_chanel_loc[0])
    # get config connection with Telegram
    cwd = os.getcwd()
    work_dir = cwd.split('ETL_sistems')
    name = f'{work_dir[0]}/ETL_sistems/config/telegram.json'
    api_id, api_hash, username, phone = get_config(name)
    # print(api_id, api_hash, username, phone)

    client = TelegramClient(username, api_id, api_hash)
    await client.start()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    # Work with channel name_chanel_loc
    user_input_channel = name_chanel_loc[0]

    # get all users of chanel
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)
    name_file_mes = f'{work_dir[0]}/ETL_sistems/datasets_com/AGI/' + name_chanel_loc[0].split('/')[-1] + '_Mes3.txt'

    # get all messages of chanel
    limit = 100
    k = 0
    global_key = True
    id_mm = name_chanel_loc[1]
    last_id = name_chanel_loc[1]
    new_last_id = 0
    while global_key:
        # print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=new_last_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=name_chanel_loc[1],
            hash=0
        ))
        messages = history.messages
        if len(messages) > 0:
            with open(name_file_mes, 'a', encoding='utf 8') as ff:
                for message in messages:
                    # print(message.id)
                    if message.id > last_id:
                        ff.write("<============================>\n")
                        mmrez = message.to_dict()
                        new_last_id = message.id
                        if message.id > id_mm:
                            id_mm = message.id
                        for mm in mmrez:
                            ff.write(f"{mm} : {mmrez[mm]}\n")
                        k += 1
        else:
            global_key = False
    print('com Messeges {name_file_mes}k == ', k)
    print('last Messeges id == ', id_mm)
    client.disconnect()


def get_control_point() -> list:
    """AI is creating summary for get_control_point

    Returns:
        list: [description]
    """
    current_path = os.getcwd()
    name_file_point = current_path.split('ETL_sistems')[0] + '/ETL_sistems/getDataFromTelegram/controlPoint.csv'

    with open(name_file_point, newline='', encoding='utf 8') as f:
        reader = csv.reader(f, delimiter='^')
        rez = []
        for row in reader:
            if row[1].isdigit():
                rez.append([row[0], int(row[1])])
    return rez


if __name__ == '__main__':
    list_name = get_control_point()
    pprint(list_name)
    # asyncio.run(get_info_chanel_num(list_name[0]))
    for name_chanel in list_name:
        print(name_chanel)
        asyncio.run(get_info_chanel_num(name_chanel))
        print()
