import jmespath
import pandas as pd
import requests
from jmespath import functions


class CustomFunctions(functions.Functions):

    @functions.signature({'types': ['string']})
    def _func_point_to_coordinates(self, s):
        longitude, latitude = s.replace('Point(', '').replace(')', '').split(' ')
        return {'longitude': longitude, 'latitude': latitude}


options = jmespath.Options(custom_functions=CustomFunctions())

endpoint_url = "https://query.wikidata.org/sparql"

all_seas_query = """
SELECT DISTINCT ?item ?itemLabel ?o WHERE {
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        {
            SELECT DISTINCT ?item ?o  WHERE {
                {
                    ?item p:P31 ?statement0 ;
                          wdt:P625 ?o.
                    ?statement0 (ps:P31/(wdt:P279*)) wd:Q204894.
                }
                UNION {
                    ?item p:P31 ?statement0 ;
                          wdt:P625 ?o.
                    ?statement0 (ps:P31/(wdt:P279*)) wd:Q165.
                }
            }
        }
}
"""

all_oceans_query = """
SELECT DISTINCT ?item ?itemLabel ?o WHERE {  
SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
  {
    SELECT DISTINCT ?item ?o  WHERE {

      ?item p:P31 ?statement0 ;
            wdt:P625 ?o.
      ?statement0 (ps:P31/(wdt:P279*)) wd:Q9430. # wd:Q15324.
    }

    LIMIT 1000
  }

}
"""


def get_results(endpoint_url, query):
    headers = {
        'accept': "application/sparql-results+json"
    }
    response = requests.request("GET", endpoint_url, headers=headers, params={'query': query})
    return response.json()


sea_results = get_results(endpoint_url, all_seas_query)
ocean_results = get_results(endpoint_url, all_oceans_query)

jpquery = jmespath.compile("""
@.results.bindings[].{ 
    name: @.itemLabel.value,
    coordinates: point_to_coordinates(o.value)
} | [].{
    name: @.name,
    latitude: @.coordinates.latitude,
    longitude: @.coordinates.longitude
} 
""")
result = []

for item in jpquery.search(sea_results, options=options):
    result.append(dict(**item, type='sea'))

for item in jpquery.search(ocean_results, options=options):
    result.append(dict(**item, type='ocean'))

pd.DataFrame(result).to_csv('sea/data/points.csv', index=False)
