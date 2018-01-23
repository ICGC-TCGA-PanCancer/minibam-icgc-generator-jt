import subprocess
import os
import shutil
from utils import get_task_dict, save_output_json
import sys

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

docker_container = "quay.io/baminou/minibam-collab-dckr:latest"
download_source = "collab"
object_id = task_dict.get('input').get('object_id')
file_name = task_dict.get('input').get('file_name')


subprocess.check_output(['docker','pull',docker_container])
subprocess.check_output(['docker','run','-e','ACCESSTOKEN','-v',cwd+':/app',docker_container,'icgc-storage-client','--profile',download_source,'download',
                         '--object-id',object_id,'--output-dir','/app','--force'])

if not os.path.isfile(os.path.join(cwd+file_name)):
    print('Object ID: '+object_id+' could not be downloaded. Try to download with icgc-storage-client for more info.')
    exit(1)

save_output_json({
    'file': os.path.join(cwd, file_name)
})