import json
from pymongo import MongoClient
from glob import glob
import os
import ConfigParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'Dataset')

def main():
	Config = ConfigParser.ConfigParser()
	Config.read('ec2.conf')
	url = Config.get('ec2_instance', 'url', 0)
	client = MongoClient(url, 27017)
	db = client.yelp
	collection = db.yelp_data

	for filename in glob(DATA_DIR + '/*.json'):
		f = open(filename, 'r')
		for line in f.read().split('\n'):
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
	
if __name__ == '__main__':
	main()

	'''
	with open(...) as f:
    for line in f:
        <do something with line>
        '''