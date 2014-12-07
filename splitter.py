import json
from pymongo import MongoClient
from glob import glob
import os
import ConfigParser
from boto.s3.connection import S3Connection
import argparse

BASE_DIR = os.path.abspath('.')
DATA_DIR = os.path.join(BASE_DIR, 'Dataset')

def get_data_from_s3():
    conn = S3Connection()
    b = conn.get_bucket('ds205-yelpdata')
    files_to_add = []
    for f in b.list():
        key_string = str(f.key)
        if not os.path.exists(os.path.join(DATA_DIR, key_string)):
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

def load_data_lst(filename, collection):
    with open(filename, 'rU') as f:
        data = f
        for line in data:
            if line[0] == '[':
                line = line[1:]
            if line[-2] == ',':
                line = line[:-2]
            if line[-1] == ']':
                line = line[:-1]
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
    parser = argparse.ArgumentParser(description='input data for mongo upload')
    parser.add_argument('--datafile', default='default', help='filename for dataupload')
    args = parser.parse_args()
    df = args.datafile
    Config = ConfigParser.ConfigParser()
    Config.read('yelp.conf')
    url = Config.get('ec2_instance', 'url', 0)

    # set to true for testing
    dev = True
    if dev:
        client = MongoClient('localhost', 27017)
    else:
        client = MongoClient(url, 27017)
    db = client.yelp
    collection = db.yelp_data

    if df == 'default':
        files_to_add = get_data_from_s3()
        for filename in glob(DATA_DIR + '/*.json'):
            if filename.split('/')[-1] in files_to_add:
                print 'loading %s' % filename.split('/')[-1]
                if 'output' in filename:
                    load_data_lst(df, collection)
                else:
                    load_data_by_line(filename, collection)
    else:
        load_data_lst(df, collection)
    
if __name__ == '__main__':
    main()