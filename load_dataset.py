import json
from pymongo import MongoClient
from glob import glob
import os
import ConfigParser
from boto.s3.connection import S3Connection

BASE_DIR = os.path.abspath('.')
DATA_DIR = os.path.join(BASE_DIR, 'Dataset')

def get_data_from_s3():
    '''gets Yelp Dataset data saved on s3 in case not saved locally'''
    conn = S3Connection()

    #change bucket name if data in another bucket
    b = conn.get_bucket('ds205-yelpdata')
    files_to_add = []

    # Files located in a directory called dataset
    for f in b.list('dataset/', ''):
        key_string = str(f.key)
        key_string = key_string.split('/')[-1]
        print key_string
        if not os.path.exists(os.path.join(DATA_DIR, key_string)) and key_string != '':
            f.get_contents_to_filename(os.path.join(DATA_DIR, key_string))
            files_to_add.append(key_string)
    return files_to_add

def load_data_by_line(filename, collection):
    with open(filename, 'r') as f:
        for line in f:
            if line:
                try:
                    line_json = json.loads(line)
                except (ValueError, KeyError, TypeError) as e:
                    print e
                    pass
                else:
                    postid = collection.insert(line_json)
                    print 'inserted with id: ', postid
    f.close()

def main():
    '''Script only needs to be run once to upload dataset data'''
    Config = ConfigParser.ConfigParser()

    # Include Yelp credentials and ec2 credentials in yelp.conf
    Config.read('yelp.conf')
    url = Config.get('ec2_instance', 'url', 0)

    dev = True
    # if false, make sure to include a ec2_instance.conf file
    if dev:
        client = MongoClient('localhost', 27017)
    else:
        client = MongoClient(url, 27017)
    db = client.yelp
    collection = db.yelp_data

    # get data from s3 and save locally
    # if not on s3, make sure dataset data in the DATA_DIR location
    files_to_add = get_data_from_s3()
    for filename in glob(DATA_DIR + '/*.json'):
        if filename.split('/')[-1] in files_to_add:
            print 'loading %s' % filename.split('/')[-1]
            load_data_by_line(filename.split('/')[-1], collection)

if __name__ == '__main__':
    main()
