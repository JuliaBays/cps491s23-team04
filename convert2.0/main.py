# Created By: Julia Bays & Gabby Snyder
# Link to how to use https://docs.google.com/document/d/e/2PACX-1vThpW312pwETdNj2Qyh33htV_B6OGaqlAsZ2RC7tbCoOLoMKEJ_3-7NC013Yaju4uhdX0xxcsbpKWuU/pub

import csv
from pymongo import MongoClient
from bson.objectid import ObjectId

# GOTO secrets repo in SWJ to see password => then replace <password> with the secret password!!
# DO NOT FORGET TO CHANGE BACK TO <password> AFTER USING PYTHON SCRIPT
# Disclaimer, do not git commit/publish password to git repo
connection_string = "mongodb+srv://Julia:<password>@swj.wjvalxm.mongodb.net/test?retryWrites=true&w=majority"

client = MongoClient(connection_string)

db = client['test']
col = db['test']

# Set up CSV reader and header
header = ['Surname', 'First Name', 'Prefix/Title', 'Date']
csvFile = open('source.csv', 'r')
reader = csv.DictReader(csvFile)

# Iterate through each row in the CSV file and insert into MongoDB
for each in reader:
    
    surName_array = []
    firstName_array = []
    
    # Split the first name and surname fields by comma to separate out multiple names
    names = each['First Name'].split(',')
    names2 = each['Surname'].split(',')
    
    # Create a unique identifier for the MongoDB entry by concatenating the first name and surname
    # This will group entries with the same first name and surname into the same MongoDB entry
    unique_id = ''.join([name.strip() for name in names2]) + ''.join([name.strip() for name in names])

    # Check if an entry with this unique identifier already exists in MongoDB
    existing_entry = col.find_one({'_id': unique_id})
    
    # If an entry with this unique identifier already exists in MongoDB, update the existing entry
    if existing_entry:
        
        # Add the date to the existing entry for each surname
        for name2 in names2:
            for obj in existing_entry['Surname']:
                if obj['Surname'] == name2.strip():
                    obj['dates'].append(each['Date'])
                    break
        
        # Add the date to the existing entry for each first name
        for name in names:
            for obj in existing_entry['FirstNames']:
                if obj['FirstName'] == name.strip():
                    obj['dates'].append(each['Date'])
                    break
        
        # Update the existing MongoDB entry with the new dates
        col.update_one({'_id': unique_id}, {'$set': {'Surname': existing_entry['Surname'], 'FirstNames': existing_entry['FirstNames']}})
    
    # If an entry with this unique identifier does not already exist in MongoDB, create a new entry
    else:
        # Create a list of objects to hold arrays of first names and years
        for name2 in names2:
            name_obj2 = {'Surname': name2.strip(), 'dates': [each['Date']]}
            surName_array.append(name_obj2)
        
        for name in names:
            name_obj = {'FirstName': name.strip(), 'dates': [each['Date']]}
            firstName_array.append(name_obj)
        
        # Create a new MongoDB entry with the surname and first name array fields and the unique identifier
        row = {'_id': unique_id, 'Surname': surName_array, 'FirstNames': firstName_array}
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
