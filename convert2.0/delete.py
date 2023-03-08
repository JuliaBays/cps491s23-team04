
import csv
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId

# GOTO secrets repo in SWJ to see password => then replace <password> with the secret password!!
# DO NOT FORGET TO CHANGE BACK TO <password> AFTER USING PYTHON SCRIPT
# Disclaimer, do not git commit/publish password to git repo
connection_string = "mongodb+srv://snyderg3:<password>@cluster0.as96288.mongodb.net/test"

#connection_string = "mongodb+srv://gabby:eTWFWagCifM8eVgA@cluster0.dgqj828.mongodb.net/test"

client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)

db = client['testpeople']
col = db['people']

col.delete_many({})  # delete all documents in the collection
