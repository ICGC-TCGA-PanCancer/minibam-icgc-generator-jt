#!/usr/bin/env python

import os
import json
import subprocess
from utils import get_task_dict, save_output_json
import sys

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

docker_container = "quay.io/baminou/minibam-collab-dckr:latest"
subprocess.check_output(['docker','pull',docker_container])

def generate_json_payload(payload_json,analysis_id, analysis_type, experiment_aligned, experiment_library_strategy,
                          experiment_reference_genome, file_json,sample_donor_gender,sample_donor_submitter_id,
                          sample_submitter_id, sample_type, sample_specimen_class,
                          sample_specimen_submitter_id, sample_specimen_type):
    return

def run_docker_command(mount_directory, docker_container, command):
    subprocess.check_output(['docker','run','-v',mount_directory+':/app',docker_container, command])

payload_json = 'payload.json'
run_docker_command(os.getcwd(),docker_container,['python', 'SongAdapter.py','init',payload_json])
run_docker_command(os.getcwd(),docker_container,['python', 'SongAdapter.py','add:analysis_type','--input',payload_json,'--type','sequencingRead'])

run_docker_command(os.getcwd(),docker_container,['python', 'SongAdapter.py','add:experiment',
                                                 '--input',payload_json,
                                                 '--unaligned',
                                                 '--library-strategy',task_dict.get('input').get('library_strategy'),
                                                 '--reference-genome', 'GRCh37' #TODO Double-check,
                                                 ])
run_docker_command(os.getcwd(),docker_container,['python', 'SongAdapter.py','add:experiment','--input',])
