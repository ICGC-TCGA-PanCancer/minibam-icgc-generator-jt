#!/usr/bin/env python

import os
import json
import subprocess
from utils import get_task_dict, save_output_json
import sys
import time

time.sleep(2*60)

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

json_input = {}

json_input['refFile']                           = {}
json_input['refFile']['path']                   = '/refdata/Homo_sapiens_assembly19.fasta'
json_input['refFile']['class']                  = 'File'

json_input['normalBam'] = {}
json_input['normalBam']['path']                 = os.path.join(task_dict.get('input').get('input_directory'),task_dict.get('input').get('normal_bam').get('file_name'))
json_input['normalBam']['class']                = 'File'

json_input['out_dir']                           = "/var/spool/cwl"

json_input['inputFileDirectory']                = {}
json_input['inputFileDirectory']['class']       = "Directory"
json_input['inputFileDirectory']['path']        = task_dict.get('input').get('input_directory')
json_input['inputFileDirectory']['location']    = task_dict.get('input').get('input_directory')

json_input['snv-padding']                       = str(task_dict.get('input').get('snv_padding'))
json_input['sv-padding']                        = str(task_dict.get('input').get('sv_padding'))
json_input['indel-padding']                     = str(task_dict.get('input').get('indel_padding'))

json_input['tumours'] = []
for i in range(0,len(task_dict.get('input').get('tumor_bams'))):
    tmp_json = {}
    tmp_json['tumourId'] = task_dict.get('input').get('tumor_bams')[i].get('file_name').replace('.bam','')
    tmp_json['bamFileName'] = task_dict.get('input').get('tumor_bams')[i].get('file_name')
    tmp_json['oxoQScore'] = task_dict.get('input').get('tumor_bams')[i].get('oxog_score')
    tmp_json['associatedVcfs'] = []
    for j in range(0,len(task_dict.get('input').get('vcf_files'))):
        tmp_json['associatedVcfs'].append(task_dict.get('input').get('vcf_files')[i].get('file_name'))
    json_input['tumours'].append(tmp_json)

json_file = 'run.json'

with open(json_file, 'w') as f:
    json.dump(json_input, f, indent=4, sort_keys=True)

subprocess.check_output(['cwltool','--debug','--relax-path-checks','--non-strict','/home/ubuntu/pcawg-minibam/pcawg_minibam_wf.cwl',json_file])

save_output_json({
    'output_directory': os.getcwd()
})