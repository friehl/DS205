#!/usr/bin/env sh

mongoexport --db yelp --collection yelp_data --query '{"id": {$exists: true} }' --out scraped.json
