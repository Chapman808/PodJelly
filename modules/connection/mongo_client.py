import pymongo
import os
import datetime

from pymongo import mongo_client

def getMongoPass (passEnvVariable : str) -> str:
    try:
        mongoPass = os.environ.get(passEnvVariable)
        print("successfully retrieved mongoPass")
    except: 
        print(passEnvVariable + " Environment variable not set. Exiting.")
        exit(0)
    return mongoPass

def getConfiguredMongoClient ():
    mongoPass = getMongoPass("MongoPass")
    return pymongo.MongoClient(
        "mongodb+srv://podjelly_dev:" 
        + mongoPass +
        "@podjelly.nuire.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    )

