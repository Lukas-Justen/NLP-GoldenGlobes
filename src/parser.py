import json


def parse_json(file_name):
    json_file = open(file_name, "r")
    json_text = json_file.read()
    return json.loads(json_text)


parsed_json_2013 = parse_json("../data/gg2013.json")
parsed_json_2015 = parse_json("../data/gg2013.json")

print(parsed_json_2013[0]['text'])
print(parsed_json_2015[0]['text'])
