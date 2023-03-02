# Created By: Julia Bays & Gabby Snyder
# Link to how to use https://docs.google.com/document/d/e/2PACX-1vThpW312pwETdNj2Qyh33htV_B6OGaqlAsZ2RC7tbCoOLoMKEJ_3-7NC013Yaju4uhdX0xxcsbpKWuU/pub

import csv
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId

# GOTO secrets repo in SWJ to see password => then replace <password> with the secret password!!
# DO NOT FORGET TO CHANGE BACK TO <password> AFTER USING PYTHON SCRIPT
# Disclaimer, do not git commit/publish password to git repo
connection_string = "mongodb+srv://Julia:<password>@swj.wjvalxm.mongodb.net/test?retryWrites=true&w=majority"

client = MongoClient(connection_string)

db = client['SWJ']
col = db['SWJ-People']

# Set up CSV reader and header
header = ['Surname', 'FirstName', 'Prefix/Title', 'FullName', 'Date']
csvFile = open('source2.csv', 'r')
reader = csv.DictReader(csvFile)

# Iterate through each row in the CSV file and insert into MongoDB
for each in reader:

    # Create an object to hold the name information
    name_obj = {'FullName': each['FullName'], 'Surname': each['Surname'], 'FirstName': each['FirstName'], 'Prefix/Title': each['Prefix/Title'], 'dates': [each['Date']]}

    # Create an object to hold the position information (only works for one position entry)
    #pos_obj = {'Position': each['Position'], 'PositionDate': each['PositionDate']}

    # Create a string to hold the date of birth information
    dob = str(each.get('DOB', ''))

    # Create a string to hold the date of death information if it exists
    dod = str(each.get('DOD', ''))

    # Create a string to hold the date of death information if it exists
    joined = str(each.get('Joined', ''))

    # Create an array to hold the organizations information
    orgs = [org for org in [str(each.get('Org1', '')), 
                            str(each.get('Org2', '')),
                            str(each.get('Org3', '')),
                            str(each.get('Org4', '')),
                            str(each.get('Org5', '')),
                            ] if org]
    
     # Create an array and a string to hold the source information (only takes in the most recent source)
    source = each.get('Source', '').split(',')

    # Create an array and a string to hold the periodicals information (only takes in the most recent source)
    periodical = each.get('Periodical', '').split(',')

    # Create a unique identifier for the MongoDB entry by hashing the full name
    unique_id = hashlib.sha256(name_obj['FullName'].encode()).hexdigest()

    # Check if an entry with this unique identifier already exists in MongoDB
    existing_entry = col.find_one({'_id': unique_id})
    
    # If an entry with this unique identifier already exists in MongoDB, update the existing entry
    if existing_entry:

        # Add the date to the existing entry for the matching name object
        for name in existing_entry['Names']:
            if name['FullName'] == name_obj['FullName'] and name['Surname'] == name_obj['Surname'] and name['FirstName'] == name_obj['FirstName'] and name['Prefix/Title'] == name_obj['Prefix/Title']:
                name['dates'].append(each['Date'])
                break
        '''
        # Add the position information to the existing entry for the matching name object
        for pos in existing_entry['Position']:
            if pos['Position'] == pos_obj['Position']:
                pos['PositionDate'].append(pos_obj['PositionDate'])
                break
        else:
            existing_entry['Position'].append(pos_obj)
        '''
        # Update the existing MongoDB entry with the new dates
        col.update_one({'_id': unique_id}, {'$set': {'Names': existing_entry['Names'], 
                                                     'DOB': existing_entry.get('DOB', ''),
                                                     'DOD': existing_entry.get('DOD', ''),
                                                     'Joined': existing_entry.get('Joined', ''),
                                                     'Orgs': orgs,
                                                     'Source': source,
                                                     'Periodical':periodical,
                                                     }})
    
    # If an entry with this unique identifier does not already exist in MongoDB, create a new entry
    else:
        # Create a names array field with the name object
        names = [name_obj]

        # Create a positions array field with the position object
        #positions = [pos_obj]

        # Create a new MongoDB entry with the names array field and the unique identifier
        row = {'_id': unique_id, 
               'Names': names, 
               'DOB': dob, 
               'DOD': dod,
               'Joined': joined,
               'Orgs': orgs,
               'Source': source,
               'Periodical':periodical,
               }
        col.insert_one(row)
    
# Close the CSV file
csvFile.close()



############################################
# this code deletes everyone in the database
############################################

'''
db = client['test']
col = db['test']
col.delete_many({})  # delete all documents in the collection
''' 
##############################################
# this code allows to update a particular info
##############################################

'''
db = client['test']
col = db['test']

header = ['Surname', 'First Name']
csvFile = open('source2.csv', 'r')
reader = csv.DictReader(csvFile)


filter_criteria = {'Surname': "A' Beckett", 'First Name': 'Abbott'}  # specify the filter criteria to identify the user
update_query = {'$set': {'First Name': 'Leo'}}  # specify the field(s) to update
col.update_one(filter_criteria, update_query)  # update the document matching the filter criteria
'''

####################################
# this code allows to input all info
####################################

'''
db = client['test']
col = db['test']

header = ['Surname', 'First Name', 'Prefix/Title']
csvFile = open('source.csv', 'r')
reader = csv.DictReader(csvFile)

for each in reader:
    row = {}
    for field in header:
        row[field] = each[field]
    print(row)
    col.insert_one(row)
'''
