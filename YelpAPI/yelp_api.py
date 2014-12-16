import argparse
import json
import urllib2
import os
import oauth2
import ConfigParser

API_HOST = 'api.yelp.com'
DEFAULT_TERM = ''
DEFAULT_LOCATION = ''
SEARCH_LIMIT = 0
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

Config = ConfigParser.ConfigParser()
Config.read('yelp.conf')

CONSUMER_KEY = Config.get('YelpApi', 'CONSUMER_KEY', 0)
CONSUMER_SECRET = Config.get('YelpApi', 'CONSUMER_SECRET', 0)
TOKEN = Config.get('YelpApi', 'TOKEN', 0)
TOKEN_SECRET = Config.get('YelpApi', 'TOKEN_SECRET', 0)

BASE_DIR = os.path.abspath('.')
DATA_DIR = os.path.join(BASE_DIR, 'api_output')

def request(host, path, url_params=None):
    url_params = url_params or {}
    url = 'http://{0}{1}'.format(host, path)
    print url

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print 'Querying {0} ...'.format(url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    finally:
        conn.close()

    return response

def query_api(zipcode, offset):
    # params set to restaurants, but can change/remove
    # to include other businesses
    url_params = {
        'category': 'restaurants',
        'location': zipcode,
        'offset': offset
    }
    return request(API_HOST, SEARCH_PATH, url_params)

def main():
    parser = argparse.ArgumentParser(description='input data for searching yelp api')
    parser.add_argument('--zipcodefile', default = 'zips.csv', help='filename for the zipcodes')

    args = parser.parse_args()
    f = open(args.zipcodefile)

    zips = [line for line in f]
    # loop through zip codes and pull top 100 results
    # offset
    for zipcode in zips:
        zipcode = zipcode.replace('\n', '')

        offset = 0
        count = 0
        get_more = True
        max_offset = 100

        while get_more and offset < max_offset:
            try:
                output = query_api(zipcode, offset)
                fname = 'zip_' + zipcode + '_' + str(count) + '.json'
                fname = os.path.join(DATA_DIR, fname)
                if output['businesses'] != []:
                    with open(fname, 'w') as outfile:
                        json.dump(output, outfile, indent=4)
                    for i in output['businesses']:
                            count += 1
                            print i['name']
                    # update offset to with number of businesses pulled
                    offset = count
                else:
                    get_more = False

            except urllib2.HTTPError as error:
                get_more = False
                count = 0
                offset = 0
                print error

            print 'Retrieved %s businesses from zipcode %s' %(count, zipcode)

if __name__ == '__main__':
    main()
