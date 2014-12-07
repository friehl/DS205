from boto.s3.connection import S3Connection
import os

BASE_DIR = os.path.abspath('.')
DATA_DIR = os.path.join(BASE_DIR, 'Dataset')

conn = S3Connection()
b = conn.get_bucket('ds205-yelpdata')
for f in b.list():
    key_string = str(f.key)
    if not os.path.exists(os.path.join(DATA_DIR, key_string)):
        print key_string
        #f.get_contents_to_filename(os.path.join(DATA_DIR, key_string))
