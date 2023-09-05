# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_clients.ipynb.

# %% auto 0
__all__ = ['BigQuery', 'Storage']

# %% ../nbs/00_clients.ipynb 4
from fastcore.test import *
from fastcore.basics import *

# %% ../nbs/00_clients.ipynb 10
from google.cloud import bigquery

# %% ../nbs/00_clients.ipynb 11
class BigQuery:
    """
    BigQuery client generation and additional methods
    """
    def __init__(
        self, 
        project_id: str, # GCP project ID
    ): 
        self.project_id = project_id
        self.client = bigquery.Client(project_id)
        
    def __repr__(self): return f'BigQuery Object ({self.project_id})'

# %% ../nbs/00_clients.ipynb 18
from google.cloud import storage
import os

# %% ../nbs/00_clients.ipynb 19
def extract_bucket_and_path(
    gcs_uri: str, # GCS URI. Ex: gs://bucket_name/[folder_name/]file_name
):
    """
    Auxiliary function to extract bucket and relative path from URI
    """
    if gcs_uri.startswith('gs://'):
        gcs_uri = gcs_uri.replace('gs://', '')
    if gcs_uri == '':
        raise ValueError(f'The gcs_uri provided is empty. "{gcs_uri}"')

    split = gcs_uri.split("/", 1)
    bucket = split.pop(0)
    path = split[0] if split and split[0] else ""

    return bucket, path

# %% ../nbs/00_clients.ipynb 21
class Storage:
    """
    Cloud Storage client generation and additional methods
    """
    def __init__(
        self, 
    ): 
        self.client = storage.Client()
        
    def __repr__(self): return f'Cloud Storage Object'

# %% ../nbs/00_clients.ipynb 22
@patch
def download_files(
    self: Storage,
    gcs_uri: str, # GCS URI. Ex: gs://bucket_name/[folder_name/] 
    local_dir: str = "", # Local directory to download the file
    verbose: bool = True, # Boolean variable to print paths of files downloaded 
):
    """
    Download the files from a GCS location to a local directory
    """
    bucket_name, folder_path = extract_bucket_and_path(gcs_uri.rstrip('/'))

    # Get the bucket and list all blobs (files and objects) in the specified folder
    bucket = self.client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=folder_path)
    blob_list = list(blobs)

    files_downloaded = 0
    # Iterate through the blobs and download files
    for blob in blob_list:
        # Exclude folders
        if not blob.name.endswith('/'): 
            # Create the local path for the downloaded file
            new_path = os.path.join(local_dir, blob.name[len(folder_path) :].lstrip('/'))
            local_path = os.path.join(os.getcwd(), new_path)

            # Create directories if they don't exist
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # Download the file from GCS to the local path
            blob.download_to_filename(local_path)

            if verbose:
                print(f'Downloaded {blob.name} to {new_path}')

            files_downloaded += 1
    return f'No. files downloaded: {files_downloaded}'
