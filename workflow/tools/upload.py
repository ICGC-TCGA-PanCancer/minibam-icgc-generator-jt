#!/usr/bin/env python3

import os
import json
import subprocess
from utils import get_task_dict, save_output_json, get_md5
import sys

def upload_file(input_directory, study_id, payload):
    upload_container = "quay.io/baminou/dckr_song_upload"

    subprocess.check_output(['docker', 'pull', upload_container])

    subprocess.check_output(['docker', 'run',
                             '--net=host',
                             '-e', 'ACCESSTOKEN',
                             '-e', 'STORAGEURL=' + os.environ.get('STORAGEURL_COLLAB'),
                             '-e', 'METADATAURL=' + os.environ.get('METADATAURL_COLLAB'),
                             '-v', input_directory + ':/app', upload_container,
                             'upload', '-s', study_id,
                             '-u', os.environ.get('METADATAURL_COLLAB'), '-p', '/app/' + payload,
                             '-o', 'manifest.txt', '-j', 'manifest.json',
                             '-d', '/app/'])

    return json.load(open(os.path.join(input_directory,'manifest.json')))


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

payloads = task_dict.get('input').get('payloads')
input_directory = task_dict.get('input').get('input_directory')
study_id = task_dict.get('input').get('study_id')

manifests = []

for i in range(0,len(payloads)):
    manifests.append(upload_file(input_directory, study_id, payloads[i]))

save_output_json({
    'manifests': manifests
})
