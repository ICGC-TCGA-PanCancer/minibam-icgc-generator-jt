#!/usr/bin/env python3

import os
import json
import subprocess
from utils import get_task_dict, save_output_json, get_md5
import sys

import shutil

def upload_file(input_directory, study_id, payload):
    upload_container = "quay.io/baminou/dckr_song_upload"
    song_server = 'http://142.1.177.168:8080'

    subprocess.check_output(['docker', 'pull', upload_container])

    subprocess.check_output(['docker','run','-e','ACCESSTOKEN',
                             '-v', input_directory+':/app',upload_container, 'upload','-s',study_id,
                             '-u', song_server, '-p', payload,
                             '-o','manifest.txt','-j','manifest.json',
                             '-d', '/app/'])


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

save_output_json(task_dict)


payloads = task_dict.get('input').get('payloads')
input_directory = task_dict.get('input').get('input_directory')
study_id = task_dict.get('input').get('study_id')

for i in range(0,len(payloads)):
    upload_file(input_directory, study_id, payloads[i])

#save_output_json({
#    'manifest_json': os.path.join(cwd,'payload.json')
#})
