import urllib.request
import json
import dml
import prov.model
import datetime
import uuid
import pandas as pd

class mbta_stops(dml.Algorithm):
    contributor = 'aqu1'
    reads = []
    writes = ['aqu1.mbta_stops_data']
    
    def drop_stations(train_stops):
        stations = ['Alewife', 'Assembly', 'Beachmont', 'Beaconsfield', 'Bellingham Square',
                    'Box District', 'Braintree', 'Brandon Hall', 'Brookline Hills', 'Brookline Village',
                    'Capen Street', 'Central', 'Central Avenue', 'Chelsea', 'Chestnut Hill',
                    'Coolidge Corner', 'Davis', 'Dean Road', 'Eastern Avenue', 'Eliot', 'Englewood Avenue',
                    'Fairbanks', 'Harvard', 'Hawes Street', 'Kendall/MIT', 'Kent Street', 'Lechmere',
                    'Longwood', 'Malden Center', 'Milton', 'Newton Centre', 'Newton Highlands',
                    'North Quincy', 'Oak Grove', 'Porter', 'Quincy Adams', 'Quincy Center', 'Revere Beach',
                    'Riverside', 'St. Marys Street', 'St. Paul Street', 'Summit Avenue', 'Tappan Street',
                    'Valley Road', 'Waban', 'Washington Square', 'Wellington', 'Wollaston', 'Wonderland',
                    'Woodland']
                    
        for s in stations:
            train_stops = train_stops[train_stops['STATION'] != s]
            
        return train_stops
    
    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()

        # Dataset 5: MBTA T stops 
        url = 'http://maps-massgis.opendata.arcgis.com/datasets/a9e4d01cbfae407fbf5afe67c5382fde_2.csv'
        train_stops = pd.read_csv(url)
        
        train_stops = mbta_stops.drop_stations(train_stops)
        
        t_stops = pd.concat([train_stops.X, train_stops.Y], axis = 1) # select columns
        t_stops.columns = ['Longitude', 'Latitude']
        t_stops = json.loads(t_stops.to_json(orient = 'records'))
        
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('aqu1', 'aqu1')
        
        repo.dropCollection("mbta_stops_data")
        repo.createCollection("mbta_stops_data")
        repo['aqu1.mbta_stops_data'].insert_many(t_stops)
        
        repo.logout()

        endTime = datetime.datetime.now()

        return {"start":startTime, "end":endTime}
        
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('aqu1', 'aqu1')
        doc.add_namespace('alg', 'http://datamechanics.io/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('agh', 'https://opendata.arcgis.com/datasets/') # Arc GIS Hub

        this_script = doc.agent('alg:aqu1#mbta_stops', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        # MBTA Stops Report
        resource_bus_stops = doc.entity('agh:2c00111621954fa08ff44283364bba70_0.csv?outSR=%7B%22wkid%22%3A102100%2C%22latestWkid%22%3A3857%7D', {'prov:label':'MBTA Bus Stops', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        resource_t_stops = doc.entity('agh:a9e4d01cbfae407fbf5afe67c5382fde_2.csv', {'prov:label':'MBTA T-Stops', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'json'})
        get_stops = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        doc.wasAssociatedWith(get_stops, this_script)
        doc.usage(get_stops, resource_bus_stops, startTime, None, {prov.model.PROV_TYPE:'ont:Retrieval'})
        doc.usage(get_stops, resource_t_stops, startTime, None, {prov.model.PROV_TYPE:'ont:Retrieval'})

        mbta_stops = doc.entity('dat:aqu1#mbta_stops_data', {prov.model.PROV_LABEL:'MBTA Stops', prov.model.PROV_TYPE: 'ont:DataSet'})
        doc.wasAttributedTo(mbta_stops, this_script)
        doc.wasGeneratedBy(mbta_stops, get_stops, endTime)
        doc.wasDerivedFrom(mbta_stops, resource_bus_stops, get_stops, get_stops, get_stops)
        doc.wasDerivedFrom(mbta_stops, resource_t_stops, get_stops, get_stops, get_stops)
        
        repo.logout()

        return doc