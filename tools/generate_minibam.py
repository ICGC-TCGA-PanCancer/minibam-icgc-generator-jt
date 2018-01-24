#!/usr/bin/env python

import os
import json
import subprocess
from utils import get_task_dict, save_output_json
import sys

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()


docker_container = "quay.io/baminou/minibam-collab-dckr:latest"


json_input = {}

json_input['refFile']                           = {}
json_input['refFile']['path']                   = '/Homo_sapiens_assembly19.fasta'
json_input['refFile']['class']                  = 'File'

json_input['normalBam'] = {}
json_input['normalBam']['path']                 = os.path.join(task_dict.get('input').get('input_directory'),task_dict.get('normal_bam').get('file_name'))
json_input['normalBam']['class']                = 'File'

json_input['out_dir']                           = "/var/spool/cwl"

json_input['minibamName']                       = "minibam.bam"

json_input['inputFileDirectory']                = {}
json_input['inputFileDirectory']['class']       = "Directory"
json_input['inputFileDirectory']['path']        = task_dict.get('input').get('input_directory')
json_input['inputFileDirectory']['location']    = task_dict.get('input').get('input_directory')

json_input['refDataDir']                        = {}
json_input['refDataDir']['class']               = 'Directory'
json_input['refDataDir']['path']                = '/datastore/oxog_refdata'
json_input['refDataDir']['location']            = '/datastore/oxog_refdata'

json_input['tumours'] = []
for i in range(0,len(task_dict.get('input').get('tumour_bams'))):
    tmp_json = {}
    tmp_json['tumourId'] = task_dict.get('input').get('tumour_bams')[i].get('file_name').replace('.bam','')
    tmp_json['bamFileName'] = task_dict.get('input').get('tumour_bams')[i].get('file_name')
    tmp_json['oxoQScore'] = task_dict.get('input').get('tumour_bams')[i].get('oxog_score')
    tmp_json['associatedVcfs'] = []
    for j in range(0,len(task_dict.get('input').get('vcf_files'))):
        tmp_json['associatedVcfs'].append(task_dict.get('input').get('vcf_files')[i])
    json_input.append(tmp_json)


subprocess.check_output(['docker','pull',docker_container])
