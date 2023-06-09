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


map_function = '''
function(doc) {
  if (doc.type === 'city') {
    emit(doc.name, doc);
  }
}
''' 

# Connect to CouchDB
couch = couchdb.Server('http://admin:admin@localhost:5984')

db = couch['cities']

design_doc = {
  "_id": "_design/cities",
  "views": {
    "by_name": {
      "map": map_function
    }
  }
}
# Save the design document to the database with conflict handling
while True:
    try:
        # Try to save the design document
        db.save(design_doc)
        break  # Break the loop if the save is successful
    except couchdb.http.ResourceConflict:
        # If a conflict occurs, retrieve the latest revision of the design document
        latest_design_doc = db.get(design_doc["_id"])
        
        # Update the design document with the latest revision and retry the save
        design_doc["_rev"] = latest_design_doc["_rev"]

# Design document saved successfully
print("Design document saved successfully.")
