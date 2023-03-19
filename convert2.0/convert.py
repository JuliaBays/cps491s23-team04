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
    #booleans for checking if empty
    pos_none = True if row["position"] == "" else False #done
    add_none = True if (row["street"] == "" and row["neighborhood"] == "" and row["city"] == "" and row["post"] == "") else False #done
    pen_none = True if row["pen"] == "" else False #done
    dob_none = True if row["dob"] == "" else False #done
    dod_none = True if row["dod"] == "" else False #done
    prop_none = True if row["proposer"] == "" else False #done
    org1_none = True if row["org1"] == "" else False #array, if not none, and if not already there, add it
    org2_none = True if row["org2"] == "" else False 
    org3_none = True if row["org3"] == "" else False
    org4_none = True if row["org4"] == "" else False
    org5_none = True if row["org5"] == "" else False
    orgs_none = True if org1_none and org2_none and org3_none and org4_none and org5_none else False
    per_none = True if row["periodicals"] == "" else False #issues, hold as array of strings, keep whole entry per row as string, add string to array if not identical
    source_none = True if row["source"] == "" else False #same as periodicals
    other_none = True if row["other"] == "" else False #done
    joined_none = True if row["joined"] == "" else False #done

    # Create objects to hold the information
    #ARRAYS OF OBJECTS
    name_obj = {"fullname": row["fullname"], "surname": row["surname"], "first": row["first"], "title": row["title"], "years": [row["year"]]}
    pos_obj = {"position": row["position"], "years": [row["year"]]}
    add_obj = {"street": row["street"], "neighborhood": row["neighborhood"], "city": row["city"], "post": row["post"], "years": [row["year"]]}
    #STRINGS
    pen_obj = row["pen"]
    dob_obj = row["dob"]
    dod_obj = row["dod"]
    prop_obj = row["proposer"]
    other_obj = row["other"]
    joined_obj = row["joined"]
    #ARRAYS - have to build them
    org_obj = [] #unique since separated
    per_obj = []
    source_obj = []
    #build
    if not org1_none:
        org_obj.append(row["org1"])
    if not org2_none:
        org_obj.append(row["org2"])
    if not org3_none:
        org_obj.append(row["org3"])
    if not org4_none:
        org_obj.append(row["org4"])
    if not org5_none:
        org_obj.append(row["org5"])
    #print("orgs object: ", org_obj)
    if not per_none:
        per_obj = row["periodicals"]
        print("per_obj: ", per_obj)
    if not source_none: 
        source_obj = row["source"]
        print("source_obj: ", source_obj)

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
        #STRINGS
        if not pen_none:
            col.update_one({"_id": unique_id}, {"$set": {"pen": pen_obj}})
        if not dob_none: 
            col.update_one({"_id": unique_id}, {"$set": {"dob": dob_obj}})
        if not dod_none:
            col.update_one({"_id": unique_id}, {"$set": {"dod": dod_obj}})
        if not prop_none: 
            col.update_one({"_id": unique_id}, {"$set": {"proposer": prop_obj}})
        if not other_none:
            col.update_one({"_id": unique_id}, {"$set": {"other": other_obj}})
        if not joined_none: 
            col.update_one({"_id": unique_id}, {"$set": {"joined": joined_obj}})  
        #ARRAYS
        #orgs
        if not orgs_none:
            try:
                print("in try orgs***")
                for org in org_obj:
                    if org not in existing["orgs"]:
                        print("need to add this org")
                        existing["orgs"].append(org)
                col.update_one({"_id": unique_id}, {"$set": {"orgs": existing["orgs"]}})
            except:
                print("in except orgs***")
                col.update_one({"_id": unique_id}, {"$set": {"orgs": org_obj}})
        #periodicals
        if not per_none: 
            try:
                print("in try per***")
                if per_obj not in existing["periodicals"]:
                        print("new periodicals string, need to add")
                        existing["periodicals"].append(per_obj)
                col.update_one({"_id": unique_id}, {"$set": {"periodicals": existing["periodicals"]}})
            except:
                print("in except per***")
                col.update_one({"_id": unique_id}, {"$set": {"periodicals": [per_obj]}})
        #source
        if not source_none: 
            try:
                print("in try source***")
                if source_obj not in existing["source"]:
                        print("new source string, need to add")
                        existing["source"].append(source_obj)
                col.update_one({"_id": unique_id}, {"$set": {"source": existing["source"]}})
            except:
                print("in except source***")
                col.update_one({"_id": unique_id}, {"$set": {"source": [source_obj]}})

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

        #STRINGS
        if not pen_none:
            col.update_one({"_id": unique_id}, {"$set": {"pen": pen_obj}})
        if not dob_none: 
            col.update_one({"_id": unique_id}, {"$set": {"dob": dob_obj}})
        if not dod_none:
            col.update_one({"_id": unique_id}, {"$set": {"dod": dod_obj}})
        if not prop_none: 
            col.update_one({"_id": unique_id}, {"$set": {"proposer": prop_obj}})
        if not other_none:
            col.update_one({"_id": unique_id}, {"$set": {"other": other_obj}})
        if not joined_none: 
            col.update_one({"_id": unique_id}, {"$set": {"joined": joined_obj}}) 

        #ARRAYS
        if not orgs_none: 
            col.update_one({"_id": unique_id}, {"$set": {"orgs": org_obj}})
        if not per_none: 
            col.update_one({"_id": unique_id}, {"$set": {"periodicals": [per_obj]}})
        if not source_none: 
            col.update_one({"_id": unique_id}, {"$set": {"source": [source_obj]}})


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
