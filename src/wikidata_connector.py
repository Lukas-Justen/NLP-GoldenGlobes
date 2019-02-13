import pickle
from pathlib import Path

import requests
import unidecode


class WikidataConnector:

    def __init__(self):
        self.queries = {"actors": """SELECT DISTINCT ?actorLabel WHERE {
  ?actor wdt:P31 wd:Q5;
         wdt:P106 wd:Q10800557.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?actorLabel""",
                        "films": """SELECT DISTINCT ?filmLabel WHERE {
  ?film wdt:P31 wd:Q11424;
        wdt:P345 ?id;
        wdt:P577 ?date.
  FILTER (?date > "2000-01-01"^^xsd:dateTime && ?date < NOW())
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?filmLabel""",
                        "directors": """SELECT DISTINCT ?directorLabel WHERE {
  ?director wdt:P31 wd:Q5;
         wdt:P106 wd:Q2526255.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?directorLabel""",
                        "series": """SELECT DISTINCT ?seriesLabel WHERE {
  ?series wdt:P31 wd:Q5398426;
        wdt:P345 ?id;
        wdt:P580 ?date.
  FILTER (?date > "2000-01-01"^^xsd:dateTime && ?date < NOW())
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?seriesLabel"""}
        self.results = {"actors": None,
                        "films": None,
                        "directors": None,
                        "series": None}

    def call_wikidate(self, query, field_name):
        if not self.results[query]:
            file = Path("wikidata_" + query + ".txt")
            if file.exists():
                with open("wikidata_" + query + ".txt", 'rb') as f:
                    self.results[query] = pickle.load(f)
            else:
                url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
                json = requests.get(url, params={'query': self.queries[query], 'format': 'json'}).json()
                self.results[query] = self.parse_json(json, field_name)
                with open("wikidata_" + query + ".txt", 'wb') as f:
                    pickle.dump(self.results[query], f)
        return self.results[query]

    def parse_json(self, json, field_name):
        entities = []
        for item in json['results']['bindings']:
            name = item[field_name]['value']
            name = name.replace('-', ' ')
            name = name.replace(' of ', ' ')
            name = unidecode.unidecode(name)
            entities.append(name)
        entities.sort(key=len, reverse=True)
        return entities
