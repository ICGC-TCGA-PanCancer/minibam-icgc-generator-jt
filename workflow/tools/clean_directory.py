#!/usr/bin/env python

from utils import get_task_dict, save_output_json
import sys, shutil

task_dict = get_task_dict(sys.argv[1])
shutil.rmtree(task_dict.get('input').get('input_directory'))