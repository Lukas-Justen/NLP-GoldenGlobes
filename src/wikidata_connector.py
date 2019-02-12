import re

import requests

actor_query = '''SELECT DISTINCT ?actorLabel WHERE {
  ?film (wdt:P31*/wdt:P279*) wd:Q11424;
        wdt:P577 ?date;
        wdt:P161 ?actor.
  FILTER (?date > "%d-01-01"^^xsd:dateTime && ?date < "%d-12-31"^^xsd:dateTime).
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?actorLabel'''

film_query = '''SELECT DISTINCT ?filmLabel WHERE {
  ?film (wdt:P31*/wdt:P279*) wd:Q11424;
        wdt:P577 ?date;
  FILTER (?date > "%d-01-01"^^xsd:dateTime && ?date < "%d-12-31"^^xsd:dateTime).
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?filmLabel'''

director_query = '''SELECT DISTINCT ?directorLabel WHERE {
  ?film (wdt:P31*/wdt:P279*) wd:Q11424;
        wdt:P577 ?date;
        wdt:P57 ?director.
  FILTER (?date > "%d-01-01"^^xsd:dateTime && ?date < "%d-12-31"^^xsd:dateTime).
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?directorLabel'''

series_query = '''SELECT DISTINCT ?seriesLabel WHERE {
  ?series (wdt:P31*/wdt:P279*) wd:Q5398426;
        wdt:P580 ?startDate;
  FILTER (?startDate > "%d-01-01"^^xsd:dateTime && ?startDate < "%d-12-31"^^xsd:dateTime).
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
} ORDER BY ?seriesLabel'''


class WikidataConnector:

    def call_wikidate(self, query, field_name, year1, year2):
        url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
        json = requests.get(url, params={'query': query % (year1, year2), 'format': 'json'}).json()
        return self.parse_json(json, field_name)

    def parse_json(self, json, field_name):
        entities = []
        validator = re.compile(r'^[a-zA-Z\s.\-]+$')
        for item in json['results']['bindings']:
            match = validator.findall(item[field_name]['value'])
            if match and len(match[0]) > 5:
                entities.append(match[0])
        return entities


year = 2013

wikidata = WikidataConnector()
actors = wikidata.call_wikidate(actor_query, 'actorLabel', year, year)
films = wikidata.call_wikidate(film_query, 'filmLabel', year, year)
directors = wikidata.call_wikidate(director_query, 'directorLabel', year, year)
series = wikidata.call_wikidate(series_query, 'seriesLabel', year - 10, year)

print("Actors: ", actors)
print("Films: ", films)
print("Directors: ", directors)
print("Series: ", series)
