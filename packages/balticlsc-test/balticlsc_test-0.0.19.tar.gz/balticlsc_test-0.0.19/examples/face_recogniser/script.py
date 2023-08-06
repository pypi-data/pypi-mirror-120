from pymongo import MongoClient
from pymongo.errors import OperationFailure, PyMongoError

print('yolo')

try:
    client = MongoClient("mongodb://myTester:abc654@127.0.0.1:27017/")
except OperationFailure:  # TODO check if authorization error (if needed)
    print('1')
except PyMongoError as e:
    print('2')

print(client.list_databases().next())
