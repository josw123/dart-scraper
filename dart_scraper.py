from __future__ import print_function, unicode_literals

import os
import re
import dart_fss as dart
from PyInquirer import prompt
from halo import Halo

qst_nm = [
    {
        'type': 'input',
        'name': 'crp_nm',
        'message': 'Company Name'
    }
]

qst_option = [
    {
        'type': 'input',
        'name': 'start_dt',
        'message': 'Start date(default: 20120101)',
        'default': '20120101'
    },
    {
        'type': 'list',
        'name': 'separate',
        'message': 'Separate',
        'choices': ['False', 'True']

    },
    {
        'type': 'list',
        'name': 'report_tp',
        'message': 'Select report type',
        'choices': ['annual', 'half', 'quarter']
    }
]



welcome = '''
    ____             __     _____                                
   / __ \____ ______/ /_   / ___/______________ _____  ___  _____
  / / / / __ `/ ___/ __/   \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
 / /_/ / /_/ / /  / /_    ___/ / /__/ /  / /_/ / /_/ /  __/ /    
/_____/\__,_/_/   \__/   /____/\___/_/   \__,_/ .___/\___/_/     
                                             /_/                 
'''

if __name__=='__main__':
    print(welcome)
    print('by Sungwoo Jo')
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start()
    crp_list = dart.get_crp_list()
    spinner.stop()

    ans = prompt(qst_nm)

    crp_nm = ans['crp_nm']
    crp_list = crp_list.find_by_name(crp_nm)

    if not crp_list:
        print('Can not find company!')
        exit(1)

    qst_crp_list = {crp.crp_nm: crp for crp in crp_list}
    qst_crp_nm_list = list(qst_crp_list.keys())

    qst_crp = [
        {
            'type': 'list',
            'name': 'crp_nm',
            'message': 'Select Company',
            'choices': qst_crp_nm_list
        }
    ]

    asn = prompt(qst_crp)
    crp_nm = asn['crp_nm']
    crp = qst_crp_list[crp_nm]

    answers = prompt(qst_option)

    regex = re.compile(r'[0-9]{4}[0-1][0-9][0-3][0-9]')
    if not regex.search(answers['start_dt']):
        print('Invalid start date!')
        exit(1)

    start_dt = answers['start_dt']
    report_tp = answers['report_tp']
    separate = False if answers['separate'] == 'False' else True

    default_path = './{}'.format(crp.crp_nm)
    default_path = os.path.abspath(default_path)
    path_message = 'Save Path'.format(default_path)
    path_question = [
        {
            'type': 'input',
            'name': 'path',
            'message': path_message,
            'default': default_path
        }
    ]

    path_answer = prompt(path_question)

    path = os.path.abspath(path_answer['path'])
    if not os.path.exists(path):
        os.makedirs(path)
    fs_list = ['fs', 'is', 'ci', 'cf']
    fs_nm_list = {'fs': '재무상태표', 'is': '손익계산서', 'ci': '포괄손익계산서', 'cf': '현금흐름표'}
    for fs_tp in fs_list:
        fs = crp.get_financial_statement(start_dt=start_dt, fs_tp=fs_tp, report_tp=report_tp, separate=separate)
        if separate:
            label = '개별'
        else:
            label = '연결'
        filename = '{}_{}.xlsx'.format(label, fs_nm_list[fs_tp])
        file_path = os.path.join(path, filename)
        fs.to_excel(file_path)
