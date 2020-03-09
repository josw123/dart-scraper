import re
import sys
import json

from app import socketio
from app.api.api_key import check_authorized
from app.api.corp_list import get_corp_list
from app.api.globals import transmit

DOWNLOAD = 'DOWNLOAD'

report_tp_regex = re.compile(r'(Annual|Semiannual|Quarterly)')
progress_regex = re.compile(r'(\d{1,3})%')


def transmit_progress(progress, corp_code, corp_name, total, index, report_tp='Annual'):
    data = dict(report_tp=report_tp,
                progress=progress,
                corp_code=corp_code,
                corp_name=corp_name,
                total=total,
                index=index)
    transmit.data(DOWNLOAD, data)


class TqdmExtractor(object):
    def __init__(self, stderr):
        super().__init__()
        self.stderr = stderr
        self.corp = None
        self.total = None
        self.index = None

    def write(self, text):
        self.stderr.write(text)

        report_tp = report_tp_regex.search(text)
        if report_tp is not None:
            report_tp = report_tp.group(1)
            progress = progress_regex.search(text)
            if progress is not None:
                progress = progress.group(1)
                transmit_progress(progress, self.corp.corp_code, self.corp.corp_name, self.total, self.index, report_tp)

    def flush(self):
        self.stderr.flush()

    def set_info(self, corp, total, index):
        self.total = total
        self.index = index
        self.corp = corp


@socketio.on(DOWNLOAD)
def download_handler(data):
    if isinstance(data, str):
        data = json.loads(data)

    if not check_authorized():
        return

    bgn_de = data.get('bgn_de')
    end_de = data.get('end_de')
    corps = data.get('corps')
    path = data.get('path')

    separate = data.get('separate', False)
    report_tp = data.get('report_tp', 'annual')
    report_tp = report_tp.lower()

    if (bgn_de and path) is None or len(corps) == 0:
        transmit.errors(DOWNLOAD, {'msg': 'Some parameters are missing'})
        return

    corp_list = get_corp_list()

    # stderr progress extractor
    stderr = sys.stderr
    sys.stderr = TqdmExtractor(stderr)

    transmit.start(DOWNLOAD)
    total = len(corps)
    # Start
    for idx, corp_code in enumerate(corps):

        corp = corp_list.find_by_corp_code(corp_code)
        sys.stderr.set_info(corp, len(corps), index=idx)
        try:
            # Extracting START
            transmit_progress(0, corp.corp_code, corp.corp_name, total, idx)

            fs = corp.extract_fs(bgn_de=bgn_de, end_de=end_de, separate=separate, report_tp=report_tp)
            filename = '{}_{}_{}.xlsx'.format(corp.corp_name, corp.corp_code, report_tp)
            fs.save(path=path, filename=filename)

        except Exception as e:
            msg = '[{}]{} : {}'.format(corp.corp_code, corp.corp_name, str(e))
            transmit.errors(DOWNLOAD, msg)

        finally:
            # Extracting Finish
            transmit_progress(100, corp.corp_code, corp.corp_name, total, idx)
    transmit.finish(DOWNLOAD)

    # Reset stderr
    sys.stderr = stderr

