#!/usr/bin/python

import math, os
import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto.s3.connection

# Connect to S3

AWS_ACCESS_KEY_ID = 'AKIAJ6P3OIYAWLS2KEIQ'
AWS_SECRET_ACCESS_KEY = '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'
Bucketname = 'lab-test-log-dc' 

conn = boto.s3.connect_to_region('s3-us-west-2.amazonaws.com',
       aws_access_key_id=AWS_ACCESS_KEY_ID,
       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
       is_secure=True,               # uncommmnt if you are not using ssl
       calling_format = boto.s3.connection.OrdinaryCallingFormat(),
       )
import boto.s3
bucket = conn.get_bucket(Bucketname)

# Get file info
source_path = 'my_test_file'
source_size = os.stat(source_path).st_size

# Create a multipart upload request
mp = b.initiate_multipart_upload(os.path.basename(source_path))

# Use a chunk size of 50 MiB (feel free to change this)
chunk_size = 52428800
chunk_count = int(math.ceil(source_size / chunk_size))

# Send the file parts, using FileChunkIO to create a file-like object
# that points to a certain byte range within the original file. We
# set bytes to never exceed the original file size.
for i in range(chunk_count + 1):
     offset = chunk_size * i
     bytes = min(chunk_size, source_size - offset)
     with FileChunkIO(source_path, 'r', offset=offset,
                         bytes=bytes) as fp:
         mp.upload_part_from_file(fp, part_num=i + 1)

# Finish the upload
mp.complete_upload()
