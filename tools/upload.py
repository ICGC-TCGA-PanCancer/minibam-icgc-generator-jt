#!/usr/bin/env python

import os
import json
import subprocess
from utils import get_task_dict, save_output_json, get_md5
import sys

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

docker_container = "quay.io/baminou/minibam-collab-dckr:latest"
subprocess.check_output(['docker','pull',docker_container])


def run_docker_command(mount_directory, docker_container, command):
    subprocess.check_output(['docker','run','-v',mount_directory+':/app',docker_container, command])

def generate_json_payload(payload_json,analysis_id, analysis_type, experiment_aligned, experiment_library_strategy,
                          experiment_reference_genome, file_json,sample_donor_gender,sample_donor_submitter_id,
                          sample_submitter_id, sample_type, sample_specimen_class,
                          sample_specimen_submitter_id, sample_specimen_type):

    run_docker_command(os.getcwd(), docker_container, ['python', 'SongAdapter.py', 'init', payload_json])

    run_docker_command(os.getcwd(), docker_container, ['python', 'SongAdapter.py', 'add:analysis_type', '--input', payload_json, '--type', analysis_type])

    return

payload_json = 'payload.json'


generate_json_payload(payload_json, None, 'sequencingRead',)

run_docker_command(os.getcwd(),docker_container,['python', 'SongAdapter.py','add:experiment',
                                                 '--input',payload_json,
                                                 '--unaligned',
                                                 '--library-strategy',task_dict.get('input').get('library_strategy'),
                                                 '--reference-genome', 'GRCh37' #TODO Double-check,
                                                 ])

minibam = task_dict.get('input').get('input_directory') + task_dict.get('input').get('normal_bam').get('minibam').get('bam_file_name')
minibai = task_dict.get('input').get('input_directory') + task_dict.get('input').get('normal_bam').get('minibam').get('bai_file_name')
run_docker_command(os.getcwd(),docker_container,['python', 'SongAdapter.py','add:file',
                                                 '--input',payload_json,
                                                 '--access',
                                                 '--md5sum',get_md5(minibam),
                                                 '--name',task_dict.get('input').get('normal_bam').get('minibam').get('bam_file_name'),
                                                 '--size',os.path.getsize(minibam),
                                                 '--type','bam'])

run_docker_command(os.getcwd(),docker_container,['python', 'SongAdapter.py','add:sample',
                                                 '--input',payload_json,
                                                 '--donor-gender',task_dict.get('input').get('donor').get('gender'),
                                                 '--donor-submitter-id',task_dict.get('input').get('donor').get('submitter_id'),
                                                 '--sample-submitter_id',task_dict.get('input').get('sample_submitter_id'),
                                                 '--sample-type', 'DNA',#TODO Double-check,
                                                 '--specimen-class','Normal',
                                                 '--specimen-submitter-id',task_dict.get('input').get('normal_bam').get('specimen').get('submitter_id'),
                                                 '--specimen-type', task_dict.get('input').get('normal_bam').get('specimen').get('type')
                                                 ])

run_docker_command(os.getcwd(),docker_container,['python', 'SongAdapter.py','validate','--input',payload_json])
