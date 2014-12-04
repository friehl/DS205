import os
import sys
import json
from glob import glob
from pymongo import MongoClient
# open each file in data directory
# clean to only get fields in yelp dataset challenge
# Upload to Mongo and check for duplicates

BASE_DIR = os.path.abspath('.')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'api_output')
URL_DIR = os.path.join(BASE_DIR, 'url_output')

class BusinessLoader:

	def __init__(self):
		self.client = MongoClient('localhost', 27017)
		self.db = self.client.yelp_test
		self.collection = self.db.businesses
		self.urls = []

		self.clean_data()
		self.output_urls()

	def get_json(self, filename):
		with open(filename, 'rb') as f:
			data = json.load(f)
			f.close()
			return data

	def load_data(self, dct):
		# Need to check for dupes
		dupe = self.collection.find_one({'id': dct['id']})
		#print dupe
		if dupe == None:
			postid = self.collection.insert(dct)
			self.urls.append(self.get_val(dct, 'url'))
			print 'inserted with id: ', postid
		else:
			print 'duplicate with id', dct['id']

	def get_val(self, dct, key):
		try:
			return dct[key]
		except KeyError as e:
			print 'Key Error: %s' % e 
			return ''

	def clean_data(self):
		for filename in glob(DATA_DIR + '/*.json'):
			data = self.get_json(filename)
			print filename
			for i in data['businesses']:
				biz = {
					'type': 'business',
					'id': self.get_val(i, 'id'),
					'business_id': '',
					'neighborhoods': self.get_val(i['location'], 'neighborhoods'),
					'full_address': self.get_val(i['location'], 'display_address'),
					'city': self.get_val(i['location'], 'city'),
					'state': self.get_val(i['location'], 'state_code'),
					'latitude': self.get_val(i['location']['coordinate'], 'latitude'),
					'longitude': self.get_val(i['location']['coordinate'], 'longitude'),
					'stars': self.get_val(i, 'rating'),
					'review_count': self.get_val(i, 'review_count'),
					'categories': self.get_val(i, 'categories'),
					'open': self.get_val(i, 'is_closed'),
					'hours': {},
					'attributes': {},
					'url': self.get_val(i, 'url'),
					'name': self.get_val(i, 'name')
				}
			
				self.load_data(biz)

	def output_urls(self):
		with open(os.path.join(URL_DIR, 'urls.txt'), 'w') as fout:
			for i in self.urls:
				fout.write(i+'\n')
		fout.close()

# Take path to yelp API json data as command line argument
def main():
	BusinessLoader()
	

if __name__ == '__main__':
	main()