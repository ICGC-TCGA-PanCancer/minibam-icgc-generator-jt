#!/usr/bin/env python

import subprocess
import os
from utils import get_task_dict, save_output_json
import sys
from shutil import copyfile

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

def download_file(object_id, out_dir, file_name):
    docker_container = "icgc/icgc-storage-client"
    download_source = "collab"

    subprocess.check_output(['docker', 'pull', docker_container])

    subprocess.check_output(['docker','run',
                             '--net=host',
                             '-e','ACCESSTOKEN',
                             '-v',out_dir+':/app',docker_container,
                             'bin/icgc-storage-client','--profile',download_source,'download',
                             '--object-id',object_id,'--output-dir','/app','--force'])

    if not os.path.isfile(os.path.join(out_dir,file_name)):
        raise ValueError('Object ID: '+object_id+' could not be downloaded. Try to download with icgc-storage-client for more info.')


# Download normal bam file
object_id = task_dict.get('input').get('normal_bam').get('object_id')
file_name = task_dict.get('input').get('normal_bam').get('file_name')
download_file(object_id, cwd, file_name)

# Download tumour bam files
for i in range(0,len(task_dict.get('input').get('tumour_bams'))):
    object_id = task_dict.get('input').get('tumour_bams')[i].get('object_id')
    file_name = task_dict.get('input').get('tumour_bams')[i].get('file_name')
    download_file(object_id, cwd, file_name)

# Download VCF files
for i in range(0,len(task_dict.get('input').get('vcf_files'))):
    file_name = task_dict.get('input').get('vcf_files')[i].get('file_name')
    if not task_dict.get('input').get('vcf_files')[i].get('is_smufin'):
        object_id = task_dict.get('input').get('vcf_files')[i].get('object_id')
        download_file(object_id, cwd, file_name)
    else:
        copyfile(os.path.join('/icgc_smufin_calls',file_name),os.path.join(cwd,file_name))

save_output_json({
    'directory': cwd
})
