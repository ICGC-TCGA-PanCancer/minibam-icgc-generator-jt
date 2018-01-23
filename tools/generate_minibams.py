import os
import json
import subprocess


docker_container = "quay.io/baminou/minibam-collab-dckr:latest"


json_input = {}

json_input['refFile']                           = {}
json_input['refFile']['path']                   = '/Homo_sapiens_assembly19.fasta'
json_input['refFile']['class']                  = 'File'

json_input['normalBam'] = {}
json_input['normalBam']['path']                 = ''
json_input['normalBam']['class']                = 'File'

json_input['out_dir']                           = "/var/spool/cwl"

json_input['minibamName']                       = "minibam.bam"

json_input['inputFileDirectory']                = {}
json_input['inputFileDirectory']['class']       = "Directory"
json_input['inputFileDirectory']['path']        = ''
json_input['inputFileDirectory']['location']    = ''

json_input['refDataDir']                        = {}
json_input['refDataDir']['class']               = 'Directory'
json_input['refDataDir']['path']                = ''
json_input['refDataDir']['location']            = ''

json_input['tumours'] = []



subprocess.check_output(['docker','pull',docker_container])
