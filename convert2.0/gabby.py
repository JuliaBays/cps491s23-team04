# Created By: Julia Bays & Gabby Snyder
# Link to how to use https://docs.google.com/document/d/e/2PACX-1vThpW312pwETdNj2Qyh33htV_B6OGaqlAsZ2RC7tbCoOLoMKEJ_3-7NC013Yaju4uhdX0xxcsbpKWuU/pub

import csv
import hashlib
from pymongo import MongoClient
from bson.objectid import ObjectId

# GOTO secrets repo in SWJ to see password => then replace <password> with the secret password!!
# DO NOT FORGET TO CHANGE BACK TO <password> AFTER USING PYTHON SCRIPT
# Disclaimer, do not git commit/publish password to git repo
connection_string = "mongodb+srv://snyderg3:Mo8wjgxWSV8X2oQg@cluster0.as96288.mongodb.net/test"

#connection_string = "mongodb+srv://gabby:eTWFWagCifM8eVgA@cluster0.dgqj828.mongodb.net/test"

client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=True)

db = client['testpeople']
col = db['people']

# Set up CSV reader and header
header = ['surname', 'first', 'title', 'fullname', 'pen', 'dob', 'dod', 'position', 'street', 'neighborhood', 'city', 'post', 'proposer', 'org1', 'org2', 'org3', 'org4', 'org5', 'periodicals', 'source', 'other', 'joined', 'bio', 'year']
csvFile = open('sourceJulia.csv', 'r')
reader = csv.DictReader(csvFile)

for row in reader:

    # Create an object to hold the name information
    name_obj = {"fullname": row["fullname"], "surname": row["surname"], "first": row["first"], "title": row["title"], "years": [row["year"]]}
    pos_obj = {"position": row["position"], "years": [row["year"]]} #should only be used if new position
    
    #booleans for checking if empty
    pos_none = False
    if row["position"] == "":
        pos_none = True
    print("pos_none: ", pos_none)

    # Create a unique identifier for the MongoDB entry by hashing the full name
    unique_id = hashlib.sha256(name_obj["fullname"].encode()).hexdigest()

    # Check if an entry with this unique identifier already exists in MongoDB
    existing = col.find_one({"_id": unique_id})
    
    # If an entry with this unique identifier already exists in MongoDB, update the existing entry
    if existing:
        nameFound = False
        posFound = False
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

    # If an entry with this unique identifier does not already exist in MongoDB, create a new entry
    else:
        #only add if there for arrays of obj that carry years
            #names, pos, addresses
        # Create a names array field with the name object
        names = [name_obj]
        pos = [pos_obj]

        # Create a new MongoDB entry with the names array field and the unique identifier
        if pos_none:
            row = {"_id": unique_id, "names": names}
        else:
            row = {"_id": unique_id, "names": names, "positions": pos}
        col.insert_one(row)
    


# Close the CSV file
csvFile.close()





'''
    name = row["fullname"]
    print(name)

    # Create a unique identifier for the MongoDB entry by hashing the full name
    unique_id = hashlib.sha256(row['fullname'].encode()).hexdigest()

    # Check if an entry with this first and last name already exists in MongoDB
    existing = col.find_one({'_id': unique_id})

    if (existing): 
        print("found existing")
        nameFound = False
        posFound = False
        addFound = False
        # Add the date to the existing entry for objects with dates
        for name in existing["names"]:
            if name["fullname"] == row['fullname'] and name['surname'] == row['surname'] and name['first'] == row['first'] and name['title'] == row['title']:
                name['dates'].append(row['year'])
                nameFound = True
                break
        if not nameFound:
            existing["names"].append({"fullname": row["fullname"], "surname": row["surname"], "first": row["first"], "title": row["title"], "year": row["year"]})
        
        for position in existing["positions"]:
            if position["position"] == row["position"]:
                position["years"].append(row["year"])
                posFound = True
                break
        if not posFound: 
            existing["positions"].append({"position": row["position"], "years": row["year"]})
        for address in existing["addresses"]:
            if address["street"] == row["street"] and address["neighborhood"] == row["neighborhood"] and address["city"] == row["city"] and address["post"] == row["post"]:
                address["dates"].append(row["year"])
                addFound = True
                break
        if not addFound: 
            existing["addresses"].append({"street": row["street"], "neighborhood": row["neighborhood"],"city": row["city"],"post": row["post"],"years": row["year"]})
        
        # check for other info
        #'pen', 'dob', 'dod', 'proposer', 'org1', 'org2', 'org3', 'org4', 'org5', 'periodicals', 'source', 'other', 'joined', 'bio', 'year']
        if existing["pen"] is None:
            existing["pen"].append(row["pen"]) 
        if existing["dob"] is None:
            existing["dob"].append(row["dob"])        
        if existing["dod"] is None: 
            existing["dod"].append(row["dod"])

        if existing["proposer"] is None:
            existing["proposer"].append(row["proposer"]) 
        #array orgs *******************
        #array periodicals ******************
        if existing["source"] is None:
            existing["source"].append(row["source"])        
        if existing["other"] is None: 
            existing["other"].append(row["other"])
        if existing["joined"] is None:
            existing["joined"].append(row["joined"])        
        if existing["dates"] is None: 
            existing["dates"].append(row["year"])
        

        # Update the existing MongoDB entry with the new dates
        col.update_one({'_id': unique_id}, {'$set': {'names': existing['names']}})

    else:
        names_obj = {"fullname": row["fullname"], "surname": row["surname"], "first": row["first"], "title": row["title"], "year": row["year"]}
        col.insert_one(names_obj)

# Close the CSV file
csvFile.close()
'''

'''
# Iterate through each row in the CSV file and insert into MongoDB
for each in reader:
    #Start Gabby
    # Create objects to hold the info
    dob_obj = each['dob']
    dod_obj = each['dod']
    joined = each['joined']
    other = each['other']
    pen = each['pen']
    proposer = each['proposer']
    sources = [each['source']]
    orgs = [each['org1'], each['org2'], each['org3'], each['org4'], each['org5']]
    periodicals = [each['periodicals']]
    name_obj = {'surname': each['surname'], 'first': each['first'], 'title': each['title'], 'dates': [each['year']]}
    positions = {'position': each['position'], 'dates': each['year']}
    addresses = {'address': each['street'] + ", " + each['neighborhood'] + ", " + each['city'] + each['post']}

    # Create a unique identifier for the MongoDB entry by hashing the full name
    unique_id = hashlib.sha256(name_obj['FullName'].encode()).hexdigest()

    # Check if an entry with this first and last name already exists in MongoDB
    existing = col.find_one({'_id': unique_id})

    if existing:
        # Add the date to the existing entry for objects with dates
        for name in existing['names']:
            if name['fullname'] == name_obj['fullname'] and name['surname'] == name_obj['surname'] and name['first'] == name_obj['first'] and name['title'] == name_obj['title']:
                name['dates'].append(each['year'])
                break
        for position in existing['positions']:
            if position['position'] == positions['position']:
                position['dates'].append(each['year'])
                break
        for address in existing['addresses']:
            if address['address'] == addresses['address']:
                address['dates'].append(each['year'])
                break

        if existing['dob'] is None: 
            existing['dob'] = dob

        # Update the existing MongoDB entry with the new dates
        col.update_one({'_id': unique_id}, {'$set': {'names': existing['names']}})

    # If an entry with this first and last name does not already exist in MongoDB, create a new entry
    else:
        # Create a names array field with the name object
        names = [name_obj]

        # Create a new MongoDB entry with the names array field and the unique identifier
        row = {'dob': dob, 'dod': dod, 'joined': joined, 'other': other, 'pen': pen, 'proposer': proposer, 'sources': sources, 'orgs': orgs, 'periodicals': periodicals, 'names': names, 'positions': positions, 'addresses': addresses}
        col.insert_one(row)
    #End Gabby

# Close the CSV file
csvFile.close()
'''


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
