from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')

# Access the database
db = client['DeepWebDatabase']

# Access the collection
collection = db['keyword_url']
 
# Read all documents
for document in collection.find():
    print(document)

# Read documents with a query
# for document in collection.find({"key": "value"}):
#     print(document)