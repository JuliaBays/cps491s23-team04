# Created By: Julia Bays & Gabby Snyder
# Link to how to use https://docs.google.com/document/d/e/2PACX-1vThpW312pwETdNj2Qyh33htV_B6OGaqlAsZ2RC7tbCoOLoMKEJ_3-7NC013Yaju4uhdX0xxcsbpKWuU/pub

import csv
from pymongo import MongoClient

# goto secrets repo in SWJ to see password => then replace <password> with the secret password!!
# DO NOT FORGET TO CHANGE BACK TO <password> AFTER USING PYTHON SCRIPT
# Disclaimer, do not git commit/publish password to git repo
connection_string = "mongodb+srv://swj1894:<password>@swj.wqoytpy.mongodb.net/SWJ?retryWrites=true&w=majority"

client = MongoClient(connection_string)

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
db = client['SWJ']
col = db['SWJ-People']

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
