from csv import DictReader
from jinja2 import Environment, FileSystemLoader, select_autoescape

def format_entry(row):
  # Extract all judges' scores as Judge (Score) pairs and join as single string

  scores = [ "%s (%s)" % (val, key[6:].capitalize()) for (key, val) in row.iteritems() if "score_" in key and val is not "0" ]
  row["nice_score"] = ", ".join(scores)
  
  # Decode utf-8 names of pros, celebs, and song titles
  for key in ["professional", "celebrity", "song"]:
    row[key] = row[key].decode('utf-8')
    
  return row

results = []

with open('results.csv') as csvfile:
  results = [ format_entry(row) for row in list(DictReader(csvfile)) ]

env = Environment(
  loader=FileSystemLoader('./templates'),
  autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('search.html').stream(results=results).dump('index.html')
