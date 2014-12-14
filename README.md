# YELP DATA COLLECTION SCRIPTS
=========

This script takes as an input a list of zip codes. It then queries those zip
codes using the Yelp API and uploads the data to a mongo database. The data
are meant to resemble data from the Yelp Dataset Challenge.

Next, using a scrapy crawler, the crawler visits the webpages of the newly
gathered businesses (currently only restaurants) and pulls all of the
review text along with the user and restaurant information.

Finally, all of the review data are uploaded to mongo and a clean up script
archives all of the scraped json files and uploads them to s3

To install all dependencies: '$ pip install -r requirements'

You will need to add the following files:
```bash
$ touch .boto # add your s3 credentials
$ touch ec2.conf # add your ec2 credentials if you want to connect to a remote db
$ touch yelp.conf # add your Yelp API credentials
```

Then, input the list of zip codes you want to query to the zips.csv file

```bash
$ bin/run.sh # This will initiate a shell script
```

Finally, if you want to dump all data scraped by the scraper, run:
```bash
$ bin/get_scraped_data.sh # This will initiate a shell script
```

That's it! This isn't meant to be used extensively, but you can use this to
get reviews from specific geos and do whatever nlp analysis you need.
