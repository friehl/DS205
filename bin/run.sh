#!/usr/bin/env sh

venv/bin/python YelpAPI/yelp_api.py 
venv/bin/python YelpAPI/etl.py 
venv/bin/python scrapy crawl yelp_review_skrape -o outputla.json
venv/bin/python splitter.py
