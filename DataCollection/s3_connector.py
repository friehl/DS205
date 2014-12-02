import boto
#from boto.s3.connection import S3Connection
from boto.s3.connection import OrdinaryCallingFormat

conn = boto.connect_s3(calling_format=OrdinaryCallingFormat())
bucket = conn.get_bucket('s3://ds205yelpdata/yelpdataset')
for key in bucket.list():
	print key.name.enconde('utf-8') 