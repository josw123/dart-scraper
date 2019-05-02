import os
import sys
import json
import logging  
import socket
import asyncio
import multiprocessing as mp

import dart_fss as dart

HOST = '127.0.0.1'          
PORT = [8989, 9898, 7878, 6767]

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger('DartScraper')

def data_encode(opcode = None, data = None):
    
    if not opcode:
        opcode = 'null'
    if not data:
        data ='null'

    raw = {'opcode': str(opcode), 'data': str(data)}
    res = json.dumps(raw).encode('utf-8')
    return res

loop = asyncio.get_event_loop()
server = None

def exception_handler(loop, context):
    print("Exception")
    loop.stop()
    loop.close()
    sys.exit()

async def task_handler(client):
    unpack = {'opcode': None}
    while unpack.get('opcode') != 'dart_shut_down':
        recv = (await loop.sock_recv(client, 1024))
        
        packet = recv.decode('utf-8')
        unpack = json.loads(packet)
        if unpack.get('opcode') == 'dart_shut_down':
            break
        
        res = dart_recv(unpack)
        await loop.sock_sendall(client, res)
    client.close()


async def run_server():
    global loop
    while True:
        client, _ = await loop.sock_accept(server)
        loop.create_task(task_handler(client))

def dart_scraper_server():
    global loop
    global server
    for port in PORT:
        server = socket_bind(port)
        if server:
            break
    
    if server is None:
        logger.critical('')
        sys.exit(-1)
    server.listen()
    server.setblocking(False)
    loop.set_exception_handler(exception_handler)
    loop.run_until_complete(run_server())


def socket_bind(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, port))
        logger.info('Socket Open. Port: ' + str(port))
        return s
    except:
        s.close()
        logger.warning('Bind failed. Port: ' + str(port))
        return None


def dart_recv(recv):
    opcode = recv.get('opcode')
    if not opcode:
        return data_encode(None, None)
    data = recv.get('data')
    opcode_handler = {
        'dart_set_api_key': dart_set_api_key,
        'dart_get_api_key': dart_get_api_key,
        'dart_get_crp_list': dart_get_crp_list,
        'dart_find_by_name': dart_find_by_name,
        'dart_download_file': dart_download_file,
        'dart_shut_down': dart_shut_down
    }
    res = opcode_handler[opcode](data)
    return res


def dart_set_api_key(api_key):
    dart.dart_set_api_key(api_key)
    return data_encode('success', dart.crp.DartAuth().api_key)


def dart_get_api_key(_):
    try:
        api_key = dart.crp.DartAuth().api_key
        return data_encode('success', api_key)
    except ValueError:
        return data_encode('error')


crp_list = None

def dart_get_crp_list(_):
    global crp_list
    crp_list = dart.get_crp_list()
    return data_encode('success', crp_list)


def dart_find_by_name(crp_nm):
    global crp_list
    if crp_list is None:
        crp_list = dart.get_crp_list()
    
    found_crp = crp_list.find_by_name(crp_nm)
    return data_encode('success', found_crp)


def dart_save_file(crp, path, start_dt, end_dt, report_tp, separate):
    save_path = os.path.abspath(path)
    if not os.path.exists(path):
        os.makedirs(path)

    fs_list = ['fs', 'is', 'ci', 'cf']
    fs_nm_list = {'fs': '재무상태표', 'is': '손익계산서', 'ci': '포괄손익계산서', 'cf': '현금흐름표'}
    logger.info('Extracting {}'.format(crp))
    for fs_tp in fs_list:
        fs = crp.get_financial_statement(start_dt=start_dt, end_dt=end_dt, fs_tp=fs_tp, report_tp=report_tp, separate=separate)
        if separate:
            label = '개별'
        else:
            label = '연결'
        filename = '{}_{}_{}.xlsx'.format(crp.crp_nm, label, fs_nm_list[fs_tp])
        file_path = os.path.join(path, filename)
        fs.to_excel(file_path)


def dart_download_file(data):
    global crp_list
    if crp_list is None:
        crp_list = dart.get_crp_list()
    
    crp_cd_list = data.get('crp_cd_list', '0')
    separate = data.get('separate', 'false')
    if separate == 'false':
        separate = False
    else:
        separate = True
    start_dt = data.get('start_dt', '20180101')
    end_dt = data.get('end_dt')
    report_tp = data.get('report_tp', 'annual')
    path = data.get('path')

    crps = [crp_list.find_by_crp_cd(crp_cd) for crp_cd in crp_cd_list]
    crps = [crp for crp in crps if crp]

    if not crps:
         return data_encode('error')
    for crp in crps:
        dart_save_file(crp, path, start_dt, end_dt, report_tp, separate)
    return data_encode('success', crps)


def dart_shut_down(s):
    pass

if __name__=='__main__':
    if sys.platform.startswith('win'):
        # On Windows calling this function is necessary.
        mp.freeze_support()
    logger.info('Start the DartScraper server')
    dart_scraper_server()