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
tumour_bams = task_dict.get('input').get('tumour_bams')
experiment = task_dict.get('input').get('experiment')
indel_padding = task_dict.get('input').get('indel_padding')
snv_padding = task_dict.get('input').get('snv_padding')
sv_padding = task_dict.get('input').get('sv_padding')
associated_vcfs = task_dict.get('input').get('associated_vcfs')

save_output_json(task_dict)

def create_payload_json(bam, experiment, input_directory, output_file, associated_vcfs):
    donor_payload = DonorPayload(donor_gender=bam.get('sample').get('donor').get('gender'),donor_submitter_id=bam.get('sample').get('donor').get('submitter_id'))
    experiment_payload = ExperimentPayload(aligned=experiment.get('aligned'),library_strategy=experiment.get('library_strategy'),reference_genome=experiment.get('reference_genome'))

    file_path = os.path.join(input_directory,bam.get('minibam').get('bam_file_name'))
    minibam_payload = FilePayload(file_access=bam.get('minibam').get('access'),file_name=bam.get('minibam').get('bam_file_name'),
                                  md5sum=hashlib.md5(open(file_path,'rb').read()).hexdigest(),file_type='BAM',file_size=os.stat(file_path).st_size)

    file_path = os.path.join(input_directory,bam.get('minibam').get('bai_file_name'))
    minibai_payload = FilePayload(file_access=bam.get('minibam').get('access'),file_name=bam.get('minibam').get('bai_file_name'),
                                  md5sum=hashlib.md5(open(file_path,'rb').read()).hexdigest(),file_type='BAI',file_size=os.stat(file_path).st_size)

    specimen_payload = SpecimenPayload(specimen_class=bam.get('sample').get('specimen').get('class'),
                                   specimen_type=bam.get('sample').get('specimen').get('type'),
                                   specimen_submitter_id=bam.get('sample').get('specimen').get('submitter_id'))

    sample_payload = SamplePayload(donor_payload=donor_payload, sample_submitter_id=bam.get('sample').get('submitter_id'),sample_type=bam.get('sample').get('type'),
                               specimen_payload=specimen_payload)

    song_payload = SongPayload(analysis_id=bam.get('song_analysis_id'), analysis_type=bam.get('song_analysis_type'),experiment_payload=experiment_payload, sample_payloads=[], file_payloads=[], info={})
    song_payload.add_file_payload(minibam_payload)
    song_payload.add_file_payload(minibai_payload)
    song_payload.add_sample_payload(sample_payload)


    song_payload.add_info('minibam_generator',{
        'git_url': "https://github.com/ICGC-TCGA-PanCancer/pcawg-minibam",
        "dockstore": "https://dockstore.org/workflows/ICGC-TCGA-PanCancer/pcawg-minibam",
        "release": "1.0.0"
    })
    song_payload.add_info('snv_padding', snv_padding)
    song_payload.add_info('sv_padding', sv_padding)
    song_payload.add_info('isPcawg',True)
    song_payload.add_info('indelPadding',indel_padding)


    song_payload.add_info('full_size_bam', {key:bam[key] for key in ['aliquot_id','file_md5sum','file_name','file_size',
                                                                     'object_id','oxog_score','song_analysis_id']})
    song_payload.add_info('vcf_files',associated_vcfs)

    song_payload.to_json_file(output_file)


payloads = []


create_payload_json(normal_bam, experiment, input_directory, os.path.join(input_directory, 'normal_minibam.json'), associated_vcfs)
payloads.append('normal_minibam.json')

for i in range(0,len(tumour_bams)):
    create_payload_json(tumour_bams[i], experiment, input_directory, os.path.join(input_directory, 'tumour_minibam_'+str(i)+'.json'), associated_vcfs)
    payloads.append( 'tumour_minibam_'+str(i)+'.json')

save_output_json({
    'payloads': payloads
})