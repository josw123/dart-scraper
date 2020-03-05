import re
import sys
import json
import threading
import dart_fss as dart

from app import socketio
from app.utils import ThreadSafeDict
from app.utils import save_config_file

report_tp_regex = re.compile(r'(Annual|Semiannual|Quarterly)')
progress_regex = re.compile(r'(\d{1,3})%')


class TqdmExtractor(object):
    def __init__(self, stderr):
        super().__init__()
        self.stderr = stderr
        self.crop_code = None

    def write(self, text):
        self.stderr.write(text)

        report_tp = report_tp_regex.search(text)
        if report_tp is not None:
            report_tp = report_tp.group(1)
            progress = progress_regex.search(text).group(1)
            data = dict(report_tp=report_tp, progress=progress, corp_code=self.crop_code)
            payload = dict(type='progress', data=data)
            socketio.emit('download', payload, broadcast=True)

    def flush(self):
        self.stderr.flush()

    def set_corp_code(self, corp_code):
        self.crop_code = corp_code


@socketio.on('connect')
def connect():
    print('connected')


@socketio.on('disconnect')
def disconnect():
    print('disconnected')


cache = ThreadSafeDict()
sem = threading.Semaphore()


def corp_list_loading():
    # Acquire semaphore
    sem.acquire()

    corp_list = cache.get('corp_list')
    if corp_list is None:
        corp_list = dart.get_corp_list()
        corp_list.load()
        cache['corp_list'] = corp_list

    # Release semaphore
    sem.release()

    return corp_list


@socketio.on('corp_list')
def corp_list_handler(data):

    # Loading Start
    payload = dict(type='loading', data='start')
    socketio.emit('corp_list', payload, broadcast=True)

    corp_list = corp_list_loading()

    # Loading Finish
    payload = dict(type='loading', data='finish')
    socketio.emit('corp_list', payload, broadcast=True)

    if isinstance(data, str):
        data = json.loads(data)
    corp_name = data.get('corp_name')
    exactly = data.get('exactly')
    if corp_name is None:
        payload = dict(type='error', data='corp_name is None')
        socketio.emit('corp_list', payload, broadcast=True)
    else:
        corps = corp_list.find_by_corp_name(corp_name=corp_name, exactly=exactly)
        payload = dict(type='data', data=[x.to_dict() for x in corps])
        socketio.emit('corp_list', payload, broadcast=True)


def set_api_key(key):
    try:
        dart.set_api_key(key)
        save_config_file({'DART_API_KEY': key})
        return True
    except dart.errors.APIKeyError:
        return False


@socketio.on('download')
def download_handler(data):
    data = json.loads(data)

    # Set DART_API_KEY
    key = data.get('api_key')
    if not set_api_key(key):
        payload = dict(type='error', data='Invalid API Key')
        socketio.emit('download', payload, broadcast=True)
        return

    bgn_de = data.get('bgn_de')
    end_de = data.get('end_de')
    corps = data.get('corps')
    path = data.get('path')

    separate = data.get('separate', False)
    report_tp = data.get('report_tp', 'annual')
    report_tp = report_tp.lower()

    if (key and bgn_de and path) is None or len(corps) == 0:
        # Error
        payload = dict(type='error', data='Some parameters are missing')
        socketio.emit('download', payload, broadcast=True)
        return

    # Loading Start
    payload = dict(type='crop_list_loading', data='start')
    socketio.emit('download', payload, broadcast=True)

    corp_list = corp_list_loading()

    # Loading Start
    payload = dict(type='crop_list_loading', data='finish')
    socketio.emit('download', payload, broadcast=True)

    # Acquire semaphore
    sem.acquire()

    # stderr progress extractor
    stderr = sys.stderr
    sys.stderr = TqdmExtractor(stderr)

    # Start
    for idx, corp_code in enumerate(corps):
        try:
            # Extracting START
            payload_data = dict(corp_code=corp_code, state='start', total=len(corps), index=idx + 1)
            payload = dict(type='download', data=payload_data)
            socketio.emit('download', payload, broadcast=True)

            sys.stderr.set_corp_code(corp_code)

            corp = corp_list.find_by_corp_code(corp_code)
            fs = corp.extract_fs(bgn_de=bgn_de, end_de=end_de, separate=separate, report_tp=report_tp)

            fs.save(path=path)

            # Extracting Finish
            payload_data = dict(corp_code=corp_code, state='finish', total=len(corps), index=idx + 1)
            payload = dict(type='download', data=payload_data)
            socketio.emit('download', payload, broadcast=True)
        except:
            # Extracting START
            payload_data = dict(corp_code=corp_code, state='error', total=len(corps), index=idx + 1)
            payload = dict(type='download', data=payload_data)
            socketio.emit('download', payload, broadcast=True)

    # Reset stderr
    sys.stderr = stderr

    # Release semaphore
    sem.release()
