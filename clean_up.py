from boto.s3.connection import S3Connection
from boto.s3.key import Key
from glob import glob
import os

BASE_DIR = os.path.abspath('.')
DATA_DIR = os.path.join(BASE_DIR, 'Dataset')

def get_archive_dir(cur_dir):
    return os.path.join(cur_dir, 'archive')

def put_in_s3(fname, s3name, cur_dir=BASE_DIR):
    '''puts a file in s3 bucket for permanent storage after it has
    been uploaded to Mongo'''
    conn = S3Connection()
    b = conn.get_bucket('ds205-yelpdata')
    match = True
    count = 0
    while match:
        for f in b.list():
            # Since the output files from the scraper have the same name
            # we increment the version - could be better, but simple for
            # a backup storage on s3
            if str(f.key) == s3name:
                s3name = str(f.key).split('_')
                s3name = 'v' + str(count) + '_' + s3name[-1]
                count += 1
                break
        else:
            match = False

    k = Key(b)
    k.key = s3name
    fname = os.path.join(cur_dir, fname)
    try:
        k.set_contents_from_filename(fname)
    except IOError as e:
        print 'error ', e
        pass

def archive_file(fname, cur_dir=BASE_DIR):
    '''Archives files in an archive folder in locally directory
    this is safer than removing the data locallly after uploading to s3, but
    there is no reason to reference it again'''

    fname = os.path.join(cur_dir, fname)
    archive_dir = get_archive_dir(cur_dir)
    try:
        os.rename(fname, os.path.join(archive_dir, fname.split('/')[-1]))
        print 'archived %s' % fname
    except OSError as e:
        print 'error ', e
        pass

def archive_api_output(foldername):
    '''archives the raw yelp api output locally'''
    floc = os.path.join(BASE_DIR, foldername)
    print floc
    for filename in glob(floc + '/*.json'):
        archive_file(filename.split('/')[-1], floc)
        print 'archived %s' % filename

def main():
    print 'starting file clean up'
    print 'uploading scraped reviews'
    put_in_s3('output.json', 'reviews.json')
    print 'archiving reviews'
    archive_file('output.json')
    print 'archiving urls'
    archive_file('urls.txt', 'url_output')
    print 'uploading business json'
    for filename in glob(os.path.join(BASE_DIR, 'api_output') + '/*.json'):
        put_in_s3(filename.split('/')[-1], filename.split('/')[-1], 'api_output')
    print 'archiving api_output'
    archive_api_output('api_output')

if __name__ == '__main__':
    main()
