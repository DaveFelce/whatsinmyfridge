curl -XPOST -u elastic:NXo9f3HaPrUq 'localhost:9200/whatsinmyfridge/recipe/_delete_by_query?conflicts=proceed&pretty' -d'
{
    "query": {
        "match_all": {}
    }
}'

# http://localhost:9200/whatsinmyfridge/recipe/_search
