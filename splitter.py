import json
from pymongo import MongoClient
import os
import ConfigParser


BASE_DIR = os.path.abspath('.')
DATA_DIR = os.path.join(BASE_DIR, 'Dataset')

def load_data_lst(filename, collection):
    '''Loads data from scrapy spider, lines are string lists'''
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
    Config = ConfigParser.ConfigParser()
    Config.read('yelp.conf')
    url = Config.get('ec2_instance', 'url', 0)

    # set to true for testing
    # otherwise, make sure to include ec2_instance.conf file
    dev = True
    if dev:
        client = MongoClient('localhost', 27017)
    else:
        client = MongoClient(url, 27017)
    db = client.yelp
    collection = db.yelp_data

    load_data_lst('output.json', collection)

if __name__ == '__main__':
    main()
