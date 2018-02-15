#!/usr/bin/env python

from utils import get_task_dict, save_output_json
import sys, shutil
import os

task_dict = get_task_dict(sys.argv[1])

input_dir = task_dict.get('input').get('input_directory')
if os.path.isdir(input_dir):
    shutil.rmtree(input_dir)