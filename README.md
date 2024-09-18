# IR Project

Repository for IR course project.

## Enabling CORS in Solr

See this website: https://laurenthinoul.com/how-to-enable-cors-in-solr/.

## How to Run

To crawl the websites for data:

```
scrapy crawl <spider-name> -O data/<filename>.json [--logfile mylog.log]
```

To index the data:

```
bin/solr start -e cloud
bin/post -c <collection-name> <project-root>/data/*
```

Then, at http://localhost:8983/solr, add a new field and 5 new copy fields such that the `managed-schema.xml` file contains the following lines:

```
...
<field name="all" type="text_general" uninvertible="true" indexed="true" stored="true"/>
...
<copyField source="author" dest="all"/>
<copyField source="description" dest="all"/>
<copyField source="subjects" dest="all"/>
<copyField source="title" dest="all"/>
<copyField source="url" dest="all"/>
...
```

Now, open `index.html` and start searching!

To clean up:

```
bin/solr delete -c <collection-name>
bin/solr stop -all
```
