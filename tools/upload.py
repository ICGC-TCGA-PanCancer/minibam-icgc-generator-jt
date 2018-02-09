#!/usr/bin/env python

import os
import json
import subprocess
from utils import get_task_dict, save_output_json, get_md5
import sys
import shutil


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()


payload_container = "quay.io/baminou/dckr_song_generate_payload"
subprocess.check_output(['docker','pull',payload_container])

input_directory = task_dict.get('input').get('input_directory')
donor = task_dict.get('input').get('donor')
experiment_library_strategy = task_dict.get('input').get('experiment_library_strategy')
normal_minibam_name = task_dict.get('input').get('normal_bam').get('minibam').get('bam_file_name')
normal_minibai_name = task_dict.get('input').get('normal_bam').get('minibam').get('bai_file_name')
tumour_bams = task_dict.get('input').get('tumour_bams')
study_id = task_dict.get('input').get('project_code')

save_output_json({
    'payload_json': task_dict.get('input')
})

song_server = 'http://142.1.177.168:8080'

subprocess.check_output(['docker','run','-v',input_directory+':/app',payload_container,'generate','-d',donor.get('id'),
                         '-st',"DNA",'-at','sequencingRead','-l',experiment_library_strategy,
                         '-o','/app/payload.json',
                         '--paired-end',
                         '-f','/app/'+normal_minibam_name,'/app/'+normal_minibai_name])

#shutil.move(os.path.join(input_directory,'payload.json'), os.path.join(cwd,'payload.json'))

#subprocess.check_output(['docker','run','-e','ACCESSTOKEN','-v',cwd+':/app',docker_container,'upload_with_song.py','-s',study_id,
                         #'-u',song_server,'-p','payload.json','-o','/app/manifest.txt'])

#for tumour_bam in tumour_bams:
#    subprocess.check_output(['docker','run','-v',input_directory+':/app',docker_container,'generate_song_payload.py','-d',donor_id,
#                             '-st',"DNA",'-at','sequencingRead','-l',experiment_library_strategy,
#                             '-o','/app/payload.json',
#                             '--paired-end',
#                             '-f','/app/'+tumour_bam.get('minibam').get('bam_file_name'),
#                             '/app/'+tumour_bam.get('minibam').get('bam_file_name')])

#shutil.move(os.path.join(input_directory,'payload.json'), os.path.join(cwd,'payload.json'))

#subprocess.check_output(['docker','run','-e','ACCESSTOKEN','-v',cwd+':/app',docker_container,'upload_with_song.py','-s',study_id,
#                         '-u',song_server,'-p','payload.json','-o','/app/manifest.txt'])



#save_output_json({
#    'payload_json': os.path.join(cwd,'payload.json')
#})
