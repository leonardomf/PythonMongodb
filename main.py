import pymongo
from pymongo import MongoClient
from flask import Flask, jsonify
import bson.json_util as json_util
import json
import certifi


client = MongoClient("mongodb+srv://admin:rootadmin@cluster0.uzp3f5v.mongodb.net/materia?retryWrites=true&w=majority", tlsCAFile=certifi.where())

app = Flask(__name__)
@app.route('/')
def homepage():
    db = client["materia"]
    collection = db["records"]

    x = collection.find()
    # tentar com o .pretty()  collection.find().pretty()
    y=json_util.dumps(x,default=json_util.default)
    return venv.loads(y)


if __name__ == '__main__':
    app.run(host='0.0.0.0:8080/json',debug=True)


