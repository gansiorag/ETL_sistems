'''
 This module make 
    
Athor: Gansior Alexander, gansior@gansior.ru, +79173383804
Starting 2022/02/04
Ending 2022//
    
'''
import json
from telethon import TelegramClient 
from telethon import connection

# для корректного переноса времени сообщений в json
from datetime import date, datetime

# классы для работы с каналами
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest

def get_config(name_file:str):
    with open(name_file) as f:
        d = json.load(f)
        return d['api_id'], d['api_hash'], d['username']
        
    
    
def prog2():
    pass
    
    
if __name__ == '__main__':
    name='/home/al/Projects_My/ETL_sistems/config/telegram.json'
    api_id, api_hash, username = get_config(name)
    print(api_id, api_hash, username)
    # The first parameter is the .session file name (absolute paths allowed)
    with TelegramClient(username, api_id, api_hash) as client:
        client.loop.run_until_complete(client.send_message('me', 'Hello, myself!'))
    prog2()