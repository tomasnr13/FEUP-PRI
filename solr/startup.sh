#!/bin/bash

precreate-core jokes
# Start Solr in background mode so we can use the API to upload the schema
solr start
# Schema definition via API
curl -X POST -H 'Content-type:application/json' --data-binary @schema/s2.json http://localhost:8983/solr/jokes/schema
# Populate collection 
#bin/post -c jokes all_jokes.json
curl -X POST -H 'Content-type:application/json' --data-binary @all_jokes.json http://localhost:8983/solr/jokes/update?commit=true
# Restart in foreground mode so we can access the interface
solr restart -f
