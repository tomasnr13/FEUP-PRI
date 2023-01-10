FROM solr:8.10

COPY all_jokes.json all_jokes.json

COPY schema.json schema.json

COPY startup.sh startup.sh

ENTRYPOINT ["bash", "startup.sh"]
