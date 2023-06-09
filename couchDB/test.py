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


""" map_function = '''
function(doc) {
  if (doc.type === 'city') {
    emit([doc.country_name, doc.state_name], doc);
  }
}
''' """

# Connect to CouchDB
couch = couchdb.Server('http://admin:admin@localhost:5984')

"""db = couch['cities']

design_doc = {
  "_id": "_design/cities",
  "views": {
    "by_country_state": {
      "map": map_function
    }
  }
}
db.save(design_doc) """


# Specify the country and state
country = 'Austria'
state = 'Tyrol'

# List of databases to search
databases = couch['cities']  # Replace with your actual database names


        
        # Query the view for the specific country and state
result = databases.view('cities/by_country_state', key=[country, state])
        
        # Iterate over the result and retrieve the city information
for row in result:
    city_info = row.value['name']
    # Process the city information as needed
    print(city_info)