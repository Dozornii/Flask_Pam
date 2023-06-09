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
countries_db = couch['countries']
states_db = couch['states']

# Query the cities database to get the city document
city_result = cities_db.view('cities/by_name', key=city_name)


# Check if the city document exists
if city_result.total_rows > 0:
    city_doc = city_result.rows[0].value
    
    # Get the state information from the states database
    state_name = city_doc['state_name']
    city_latitude = city_doc['latitude']
    city_longitude = city_doc['longitude']
  
    state_doc = states_db.view('states/by_name', key=state_name)
    state_doc = state_doc.rows[0].value
    #print(state_name)
    # Get the country information from the countries database
    country_name = city_doc['country_name']
    country_doc = countries_db.view('countries/by_name', key=country_name)
    country_doc = country_doc.rows[0].value
    print(country_doc)
    # Retrieve the latitude and longitude values
    


    country_latitude = country_doc['latitude']
    country_longitude = country_doc['longitude']
        # Process the city information as needed

    state_latitude = state_doc['latitude']
    state_longitude = state_doc['longitude']

    
    # Print the latitude and longitude values
    print("City Latitude:", city_latitude)
    print("City Longitude:", city_longitude)
    print("State Latitude:", state_latitude)
    print("State Longitude:", state_longitude)
    print("Country Latitude:", country_latitude)
    print("Country Longitude:", country_longitude)
else:
    print("City not found.")