#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from overture_song.model import ApiConfig
from overture_song.tools import FileUploadClient, FileUploadState

def main():
    parser = argparse.ArgumentParser(description='Upload payload using SONG')
    parser.add_argument('-i', '--input', dest="input", help="Payload file", required=True)
    parser.add_argument('-s', '--study', dest="study_id", help="Study ID", required=True)
    parser.add_argument('-a', '--access-token', dest="access_token", help="Access Token", default=os.environ.get('ACCESSTOKEN',None),required=True)
    parser.add_argument('-d', '--destination-url', dest="server_url", help="Server URL",required=True)
    results = parser.parse_args()

    config = ApiConfig(results.server_url, results.study_id, results.access_token, True)
    file_upload_client = FileUploadClient(config, results.input, True)




def upload_file_client(file_upload_client):
    file_upload_client.upload()

    if file_upload_client.upload_id is None:
        raise ValueError('Upload id is empty')
    if not file_upload_client.upload_errors is None:
        raise ValueError(file_upload_client.upload_errors[0])
    if not file_upload_client.upload_state is FileUploadState.SUBMITTED:
        raise ValueError('Payload has not been uploaded')

    file_upload_client.update_status()

    if not file_upload_client.upload_state is FileUploadState.VALIDATED:
        raise ValueError('Payload validation failed')
    if not file_upload_client.upload_errors is None:
        raise ValueError(file_upload_client.upload_errors[0])

    file_upload_client.save()

    if not file_upload_client is FileUploadState.SAVED:
        raise ValueError('Payload has not been saved')
    if not file_upload_client.upload_errors is None:
        raise ValueError(file_upload_client.upload_errors[0])
    if file_upload_client.analysis_id is None:
        raise ValueError('An error occured while saving the payload')


if __name__ == "__main__":
    main()