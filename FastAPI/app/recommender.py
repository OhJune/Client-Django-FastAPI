from google.cloud import storage
from gensim.models import Word2Vec

def download_blob(bucket_name, source_blob_name, destination_file_name):
    storage_client = storage.Client.from_service_account_json(key_path)
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    
key_path = "/home/oh/testapi/key.json"

bucket_name = "song2vec"
source_blob_name = "song2vec.model"
destination_file_name = "song2vec.model"


# 현재 경로에 다운로드 됨
download_blob(bucket_name, source_blob_name, destination_file_name)

