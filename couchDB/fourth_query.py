import couchdb
import json
#couch = couchdb.Server('http://admin:admin@localhost:5984')
#db = couch['countries']
# Load JSON file

#with open('countries.json', errors='ignore') as json_file:
#    data = json.load(json_file)

# Upload documents to CouchDB
#for doc in data:
#    db.save(doc)

#print("JSON file uploaded successfully.")


city_name = 'Heinfels'

# Connect to CouchDB
couch = couchdb.Server('http://admin:admin@localhost:5984')

cities_db = couch['cities']

view_result = cities_db.view('cities/by_country', reduce=True, group=True)
country_counts = [(row.key, row.value) for row in view_result]

# Sort the country counts in descending order based on the count value
sorted_country_counts = sorted(country_counts, key=lambda x: x[1], reverse=True)

# Get the country with the highest count
country_with_highest_cities = sorted_country_counts[0][0]
print(sorted_country_counts)

print("Country with the highest number of cities:", country_with_highest_cities)