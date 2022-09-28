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

def get_config(name_file:str):
    with open(name_file) as f:
        d = json.load(f)
        return d['api_id'], d['api_hash'], d['username'], d['api_id']
        

def getAllUsersChanel(NameChanel:str):
    # get config connection with Telegram
    cwd = os.getcwd()
    WorkDir = cwd.split('ETL_sistems')
    name=f'{WorkDir[0]}/ETL_sistems/config/telegram.json'
    api_id, api_hash, username, phone  = get_config(name)
    print(api_id, api_hash, username, phone)
    
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))
    
    # Work with channel NameChanel       
    user_input_channel = NameChanel
   
    # get all users of chanel
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = client.get_entity(entity)
    offset = 0
    limitUsers = 100
    all_participants = []
    dataText = str(datetime.now()).replace('-','_').replace(' ','_').replace(':','_').replace('.','_')
    nameFileUser = f'{WorkDir[0]}/ETL_sistems/datasets_com/AGI/' + NameChanel.split('/')[-1] +'_' + dataText +'_User.txt'   
    while True:
        participants = client(GetParticipantsRequest(
            my_channel, ChannelParticipantsSearch(''), offset, limitUsers,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
    print(f'KOl users = {offset}')
    with open(nameFileUser , 'w', encoding='utf8') as outfile:
        outfile.write("id^first_name^last_name^user^phone^is_bot\n")
        for participant in all_participants:
            name = ''
            lastName = ''
            if type(participant.first_name) == str : name = u'{}'.format(participant.first_name)
            if type(participant.last_name) == str : lastName = u'{}'.format(participant.last_name)
            #print(name, lastName, sep= ' ------- ')
            outfile.write(f"{participant.id}^{name}^{lastName}^{participant.username}^{participant.phone}^{participant.bot}\n")    
    client.disconnect()
    

def getInfoChanel(NameChanel:str):
    
    # get config connection with Telegram
    cwd = os.getcwd()
    WorkDir = cwd.split('ETL_sistems')
    name=f'{WorkDir[0]}/ETL_sistems/config/telegram.json'
    api_id, api_hash, username, phone  = get_config(name)
    print(api_id, api_hash, username, phone)
    
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))
    
    # Work with channel NameChanel       
    user_input_channel = NameChanel
   
    # get all users of chanel
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = client.get_entity(entity)
    
    # offset = 0
    # limitUsers = 100
    # all_participants = []
    nameFileUser = f'{WorkDir[0]}/ETL_sistems/datasets_com/AGI/' + NameChanel.split('/')[-1] + '_User.txt'
    nameFileMes = f'{WorkDir[0]}/ETL_sistems/datasets_com/AGI/' + NameChanel.split('/')[-1] + '_Mes.txt'
    # print(nameFileUser, nameFileMes, sep = ' --- ')
    # while True:
    #     participants = client(GetParticipantsRequest(
    #         my_channel, ChannelParticipantsSearch(''), offset, limitUsers,
    #         hash=0
    #     ))
    #     if not participants.users:
    #         break
    #     all_participants.extend(participants.users)
    #     offset += len(participants.users)
    # print(f'KOl users = {offset}')
    # with open(nameFileUser , 'w', encoding='utf8') as outfile:
    #     outfile.write("id^first_name^last_name^user^phone^is_bot\n")
    #     for participant in all_participants:
    #         name = ''
    #         lastName = ''
    #         if type(participant.first_name) == str : name = u'{}'.format(participant.first_name)
    #         if type(participant.last_name) == str : lastName = u'{}'.format(participant.last_name)
    #         #print(name, lastName, sep= ' ------- ')
    #         outfile.write(f"{participant.id}^{name}^{lastName}^{participant.username}^{participant.phone}^{participant.bot}\n")

    # get all messages of chanel
    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0
    k =0
    while True:
        #print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
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
                k +=1
        offset_id = messages[len(messages) - 1].id
        #print('k == ', k)
    print('com Messeges {nameFileMes}k == ', k)
    client.disconnect()
        
if __name__ == '__main__':
    listName = [
        #'https://t.me/ai_life',
        #'https://t.me/agirussia',
        #'https://t.me/AGIRussia_SCA',
        #'https://t.me/agiterms',
        #'https://t.me/OpenTalksAI',
        'https://t.me/agirussianews']
    for NameChanel in listName:
        getAllUsersChanel(NameChanel)
        #getInfoChanel(NameChanel)



