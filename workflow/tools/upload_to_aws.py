#!/usr/bin/env python

import os
import sys
from utils import get_md5, get_task_dict, save_output_json
import subprocess
import time
import json


allowed_codes = { 'LIRI-JP', 'PACA-CA' , 'PRAD-CA', 'RECA-EU', 'PAEN-AU', 'PACA-AU',
'BOCA-UK','OV-AU', 'MELA-AU', 'BRCA-UK', 'PRAD-UK', 'CMDI-UK', 'LINC-JP',
'ORCA-IN', 'BTCA-SG', 'LAML-KR', 'LICA-FR', 'CLLE-ES', 'ESAD-UK', 'PAEN-IT'}


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

subprocess.check_output(['docker','pull','mesosphere/aws-cli'])

def upload_file(input_directory, study_id, payload):
    upload_container = "quay.io/baminou/dckr_song_upload"
    song_server = 'http://142.1.177.168:8080'

    subprocess.check_output(['docker', 'pull', upload_container])

    subprocess.check_output(['docker', 'run',
                             '--net=host',
                             '-e', 'ACCESSTOKEN',
                             '-e', 'STORAGEURL=' + os.environ.get('STORAGEURL_AWS'),
                             '-e', 'METADATAURL=' + os.environ.get('METADATAURL_AWS'),
                             '-v', input_directory + ':/app', upload_container,
                             'upload', '-s', study_id,
                             '-u', song_server, '-p', '/app/' + payload,
                             '-o', 'manifest.txt', '-j', 'manifest.json',
                             '-d', '/app/'])

    return json.load(open(os.path.join(input_directory,'manifest.json')))


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

payloads = task_dict.get('input').get('payloads')
input_directory = task_dict.get('input').get('input_directory')
study_id = task_dict.get('input').get('study_id')

task_start = int(time.time())
run = study_id in allowed_codes

manifests = []

for i in range(0,len(payloads)):
    manifests.append(upload_file(input_directory, study_id, payloads[i]))

save_output_json({
    'manifests': manifests
})
