#!/usr/bin/env python3

from utils import get_task_dict, save_output_json

from overture_song_payload import DonorPayload
from overture_song_payload import ExperimentPayload
from overture_song_payload import FilePayload
from overture_song_payload import SpecimenPayload
from overture_song_payload import SamplePayload
from overture_song_payload import SongPayload

import sys
import os
import hashlib

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

input_directory = task_dict.get('input').get('input_directory')
normal_bam = task_dict.get('input').get('normal_bam')
tumor_bams = task_dict.get('input').get('tumor_bams')
experiment = task_dict.get('input').get('experiment')
analysis = task_dict.get('input').get('analysis')

save_output_json(task_dict)

def create_payload_json(bam, analysis, experiment, input_directory, output_file):
    donor_payload = DonorPayload(donor_gender=bam.get('sample').get('donor').get('submitter_id'),donor_submitter_id=bam.get('sample').get('donor').get('submitter_id'))
    experiment_payload = ExperimentPayload(aligned=experiment.get('aligned'),library_strategy=experiment.get('library_strategy'),reference_genome=experiment.get('reference_genome'))

    file_path = os.path.join(input_directory,bam.get('minibam').get('bam_file_name'))
    minibam_payload = FilePayload(file_access=bam.get('minibam').get('access'),file_name=bam.get('minibam').get('bam_file_name'),
                                  md5sum=hashlib.md5(open(file_path,'rb').read()).hexdigest(),file_type='BAM',file_size=os.stat(file_path).st_size)

    file_path = os.path.join(input_directory,normal_bam.get('minibam').get('bai_file_name'))
    minibai_payload = FilePayload(file_access=normal_bam.get('minibam').get('access'),file_name=normal_bam.get('minibam').get('bai_file_name'),
                                  md5sum=hashlib.md5(open(file_path,'rb').read()).hexdigest(),file_type='BAI',file_size=os.stat(file_path).st_size)

    specimen_payload = SpecimenPayload(specimen_class=bam.get('sample').get('specimen').get('class'),
                                   specimen_type=bam.get('sample').get('specimen').get('type'),
                                   specimen_submitter_id=bam.get('sample').get('specimen').get('submitter_id'))

    sample_payload = SamplePayload(donor_payload=donor_payload, sample_submitter_id=bam.get('sample').get('submitter_id'),sample_type=bam.get('sample').get('type'),
                               specimen_payload=specimen_payload)

    song_payload = SongPayload(analysis_id=analysis.get('id'), analysis_type=analysis.get('type'),experiment_payload=experiment_payload)
    song_payload.add_file_payload(minibam_payload)
    song_payload.add_file_payload(minibai_payload)
    song_payload.add_sample_payload(sample_payload)
    song_payload.add_info('isPcawg',True)
    song_payload.to_json_file(output_file)


payloads = []

create_payload_json(normal_bam, analysis, experiment, input_directory, os.path.join(input_directory, 'normal_minibam.json'))
payloads.append('normal_minibam.json')

for i in range(0,len(tumor_bams)):
    create_payload_json(tumor_bams[i],analysis, experiment, input_directory, os.path.join(input_directory, 'tumor_minibam_'+str(i)+'.json'))
    payloads.append( 'tumor_minibam_'+str(i)+'.json')

save_output_json({
    'payloads': payloads
})