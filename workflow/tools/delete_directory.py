#!/usr/bin/env python

import os
import shutil
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      input_dir:
        type: string
        is_file: true
"""
input_dir = task_dict.get('input').get('input_dir')

task_start = int(time.time())

# do the real work here
task_info = ''

try:
    shutil.rmtree(input_dir)
except:
    pass
# complete the task
task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    },
    'task_info': task_info
}

save_output_json(output_json)

if task_info.startswith('Error'):
    sys.exit(1)
