'''
 This module make 
    
Athor: Gansior Alexander, gansior@gansior.ru, +79173383804
Starting 2022/07/24
Ending 2022//
    
'''
import json
import os
import csv
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
        

def getInfoChanelNum(NameChanel: list):
    print(NameChanel[0])
    # get config connection with Telegram
    cwd = os.getcwd()
    WorkDir = cwd.split('ETL_sistems')
    name=f'{WorkDir[0]}/ETL_sistems/config/telegram.json'
    api_id, api_hash, username, phone  = get_config(name)
    #print(api_id, api_hash, username, phone)
    
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            client.sign_in(password=input('Password: '))
    
    # Work with channel NameChanel       
    user_input_channel = NameChanel[0]
   
    # get all users of chanel
    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = client.get_entity(entity)
    

    nameFileMes = f'{WorkDir[0]}/ETL_sistems/datasets_com/AGI/' + NameChanel[0].split('/')[-1] + '_Mes1.txt'
  
    # get all messages of chanel
    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0
    k =0
    globalKey = True
    while globalKey:
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
                if message.id > NameChanel[1]:
                    ff.write("<============================>\n")
                    mmrez = message.to_dict()
                    for mm in mmrez:
                        ff.write(f"{mm} : {mmrez[mm]}\n")
                    k +=1
                else:
                    globalKey = False
                    break
        offset_id = messages[len(messages) - 1].id
        #print('k == ', k)
    print('com Messeges {nameFileMes}k == ', k)
    client.disconnect()
    
    
def getControlPoint() -> list:
    currentPath = os.getcwd()
    nameFilePoint = currentPath.split('ETL_sistems')[0] + '/ETL_sistems/getDataFromTelegram/controlPoint.csv'
     
    with open(nameFilePoint, newline='') as f:
        reader = csv.reader(f, delimiter=('^'))
        rez = []
        for row in reader:
            if row[1].isdigit():
                rez.append([row[0], int(row[1])])
    return rez
            
if __name__ == '__main__':
    listName = getControlPoint()
    pprint(listName)
    for NameChanel in listName:
        getInfoChanelNum(NameChanel)



