#!/usr/bin/env python3

import os
import json
import subprocess
from utils import get_task_dict, save_output_json, get_md5
import sys

import shutil


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()


upload_container = "quay.io/baminou/dckr_song_upload"

payloads = task_dict.get('input').get('payloads')
input_directory = task_dict.get('input').get('input_directory')
normal_minibam_name = task_dict.get('input').get('normal_bam').get('minibam').get('bam_file_name')
normal_minibai_name = task_dict.get('input').get('normal_bam').get('minibam').get('bai_file_name')
tumour_bams = task_dict.get('input').get('tumor_bams')
study_id = task_dict.get('input').get('project_code')

song_server = 'http://142.1.177.168:8080'

subprocess.check_output(['docker', 'pull', upload_container])

for i in range(0,len(payloads)):
    subprocess.check_output(['docker','run','-e','ACCESSTOKEN','-v',input_directory+':/app',upload_container,'upload','-s',study_id,
                         '-u',song_server,'-p',payloads[i],'-o','/app/manifest.txt','-j','/app/manifest.json'])


#shutil.move(os.path.join(input_directory,'payload.json'), os.path.join(cwd,'payload.json'))

subprocess.check_output(['docker','run','-e','ACCESSTOKEN','-v',cwd+':/app',upload_container,'upload','-s',study_id,
                         '-u',song_server,'-p','payload.json','-o','/app/manifest2.txt','/app/manifest2.json'])



#save_output_json({
#    'payload_json': os.path.join(cwd,'payload.json')
#})
