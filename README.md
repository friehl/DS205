# YELP DATA COLLECTION SCRIPTS
=========

The goal of this script is to take a list of zip codes and retrieve all of the
restaurants and corresponding reviews and load them into MongoDB. The scripts
utilize the Yelp API, s3, scrapy and Mongo.

* load_dataset.py: This script uploads the initial Yelp Dataset Challenge
data into Mongo
* bin/run.sh: Shell script that kicks off data collection:
 * YelpAPI/yelp_api.py: reads from the zips.csv file and looks up
 restaurants in that zip. Script defaults to grabbing 100 results. Data dumps
 to json files in api_output directory
 * YelpAPI/etl.py: Uploads json files fin the api_output directory to MongoDB.
 Script checks for duplicates before uploading. After uploading, unique
 business urls are outputed to url_output for review scraping
 * scrapy crawl yelp_review_skrape: Utilizes a Scrapy spider to grab all of the
 reviews. The crawler paginates to grab every review. The scraper is here:
 yelp_review_skrape/spiders/yelp_spider.py. First time using scrapy, it's pretty
 cool.
 * splitter.py: Script uploads scraped reviews to the Mongo database. A bit of
 data cleaning was needed
 * clean_up.py: This script takes all of the .json files created by the
 aforementioned processes and uploads them to s3 (the destination bucket is
   hard-coded in the script) and then puts them in local 'archive' folders in
   case you want to inspect what you just uploaded


To install all dependencies: '$ pip install -r requirements'

You will need to add the following files:
```bash
$ touch .boto # add your s3 credentials
$ touch ec2.conf # add your ec2 credentials if you want to connect to a remote db
$ touch yelp.conf # add your Yelp API credentials
```

Then, input the list of zip codes you want to query to the zips.csv file

```bash
$ bin/run.sh # This will initiate the api and scraper
```

Finally, if you want to dump all data in MongoDB,  run:
```bash
$ bin/get_scraped_data.sh #
```

That's it! This isn't meant to be used extensively, but you can use this to
get reviews from specific geos and do whatever nlp analysis you need.
