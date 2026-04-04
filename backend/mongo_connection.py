from pymongo import MongoClient  

client = MongoClient("mongodb+srv://vaasvi_db_user:Vaasvi27@cluster0.zkv9rht.mongodb.net/?appName=Cluster0")  

db = client["ecommerce_nosql"]  

def get_mongo_db():  
    return db