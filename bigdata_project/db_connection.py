import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

def get_db():

    try:
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("DB_NAME", "bigdata_covid")
        client = MongoClient(mongo_uri)
        return client[db_name]
    
    except:
        print("Não foi possível encontrar o banco.")
