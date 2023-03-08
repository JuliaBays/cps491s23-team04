# Created By: Julia Bays & Gabby Snyder
# Link to how to use https://docs.google.com/document/d/e/2PACX-1vThpW312pwETdNj2Qyh33htV_B6OGaqlAsZ2RC7tbCoOLoMKEJ_3-7NC013Yaju4uhdX0xxcsbpKWuU/pub

import csv
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId

# GOTO secrets repo in SWJ to see password => then replace <password> with the secret password!!
# DO NOT FORGET TO CHANGE BACK TO <password> AFTER USING PYTHON SCRIPT
# Disclaimer, do not git commit/publish password to git repo
connection_string = "mongodb+srv://snyderg3:<password>@cluster0.as96288.mongodb.net/test"

client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)

db = client["testpeople"]
col = db["people"]

# Set up CSV reader and header
header = ["surname", "first", "title", "fullname", "pen", "dob", "dod", "position", "street", "neighborhood", "city", "post", "proposer", "org1", "org2", "org3", "org4", "org5", "periodicals", "source", "other", "joined", "bio", "year"]
csvFile = open("sourceJulia.csv", "r")
reader = csv.DictReader(csvFile)

for row in reader:
    # Create an object to hold the name information
    name_obj = {"fullname": row["fullname"], "surname": row["surname"], "first": row["first"], "title": row["title"], "years": [row["year"]]}
    pos_obj = {"position": row["position"], "years": [row["year"]]}
    add_obj = {"street": row["street"], "neighborhood": row["neighborhood"], "city": row["city"], "post": row["post"], "years": [row["year"]]}
    
    #booleans for checking if empty
    pos_none = False
    add_none = False
    if row["position"] == "":
        pos_none = True
    if row["street"] == "" and row["neighborhood"] == "" and row["city"] == "" and row["post"] == "":
        add_none = True
    
    pen_none = False if row["pen"] == "" else True
    dob_none = False if row["dob"] == "" else True
    dod_none = False if row["dod"] == "" else True
    prop_none = False if row["proposer"] == "" else True
    org1_none = False if row["org1"] == "" else True
    org2_none = False if row["org2"] == "" else True 
    org3_none = False if row["org3"] == "" else True
    org4_none = False if row["org4"] == "" else True
    org5_none = False if row["org5"] == "" else True
    periodicals_none = False if row["periodicals"] == "" else True
    source_none = False if row["source"] == "" else True
    other_none = False if row["other"] == "" else True
    joined_none = False if row["joined"] == "" else True

    # Create a unique identifier for the MongoDB entry by hashing the full name
    unique_id = hashlib.sha256(name_obj["fullname"].encode()).hexdigest()

    # Check if an entry with this unique identifier already exists in MongoDB
    existing = col.find_one({"_id": unique_id})
    
    # If an entry with this unique identifier already exists in MongoDB, update the existing entry
    if existing:
        nameFound = False
        posFound = False
        addFound = False
        # Add the date to the existing entry for objects with dates
        #NAMES
        for name in existing["names"]:
            if name["fullname"] == name_obj["fullname"] and name["surname"] == name_obj["surname"] and name["first"] == name_obj["first"] and name["title"] == name_obj["title"]:
                name["years"].append(row["year"])
                nameFound = True
                break
        if not nameFound: #shouldn't need this
            existing["names"].append({"fullname": row["fullname"], "surname": row["surname"], "first": row["first"], "title": row["title"], "years": [row["year"]]})
        col.update_one({"_id": unique_id}, {"$set": {"names": existing["names"]}})

        #POSITIONS
        if not pos_none:
            try:
                # Some Code
                for position in existing["positions"]:
                    if position["position"] == pos_obj["position"]:
                        position["years"].append(row["year"])
                        #remove current positions and add the new edited version
                        col.update_one({"_id": unique_id}, {"$set": {"positions": existing["positions"]}})
                        posFound = True
                        break
                if not posFound: #no existing position matches this position, add new object to positions array
                    #print("positions before: ", existing["positions"])
                    #existing["positions"].append(pos)
                    print(col.find_one({"_id": unique_id}))
                    col.update_one({"_id": unique_id}, { '$push': {"positions": pos_obj}})
                    print(col.find_one({"_id": unique_id}))
                    #print("positions after: ", existing["positions"])
                print("finished try pos")
            except: #existing["positions"] does not exist yet and there is a position to add
                print("in except pos")
                #positions not created yet
                #existing["positions"] = [pos_obj]
                col.update_one({"_id": unique_id}, {"$set": {"positions": [pos_obj]}})

        #ADDRESSES
        if not add_none:
            try:
                for address in existing["addresses"]:
                    if address["street"] == add_obj["street"] and address["neighborhood"] == add_obj["neighborhood"] and address["city"] == add_obj["city"] and address["post"] == add_obj["post"] and not add_none:
                        address["years"].append(row["year"])
                        col.update_one({"_id": unique_id}, {"$set": {"addresses": existing["addresses"]}})
                        addFound = True
                        break
                if not addFound: 
                    col.update_one({"_id": unique_id}, { '$push': {"addresses": add_obj}})
                print("finished try add")
            except: 
                print("in except add")
                #positions not created yet
                col.update_one({"_id": unique_id}, {"$set": {"addresses": [add_obj]}})

    # If an entry with this unique identifier does not already exist in MongoDB, create a new entry
    else:
        #only add if there for arrays of obj that carry years
            #names, pos, addresses
        # Create a names array field with the name object
        names = [name_obj]
        pos = [pos_obj]
        add = [add_obj]

        # Create a new MongoDB entry with the names array field and the unique identifier
        if pos_none or add_none:
            if pos_none and add_none:
                row = {"_id": unique_id, "names": names}
            elif pos_none:
                row = {"_id": unique_id, "names": names, "addresses": add}
            else: #add_none
                row = {"_id": unique_id, "names": names, "positions": pos}
        else:
            row = {"_id": unique_id, "names": names, 
                "positions": pos, 
                "addresses": add}
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
