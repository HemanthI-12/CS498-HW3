from flask import Flask, request, jsonify
from pymongo import MongoClient, WriteConcern, ReadPreference

app = Flask(__name__)

MONGO_URI = "mongodb+srv://USERNAME:PASSWORD@lab6cluster.9nu5jeu.mongodb.net/?appName=Lab6Cluster"
client = MongoClient(MONGO_URI)
db = client.ev_db
collection = db.vehicles

@app.route('/insert-fast', methods=['POST'])
def insert_fast():
    """Requirement 1: Acknowledged by Primary only."""
    data = request.json
    fast_collection = collection.with_options(write_concern=WriteConcern(w=1))
    result = fast_collection.insert_one(data)
    return str(result.inserted_id)

@app.route('/insert-safe', methods=['POST'])
def insert_safe():
    data = request.json
    safe_collection = collection.with_options(write_concern=WriteConcern(w='majority'))
    result = safe_collection.insert_one(data)
    return str(result.inserted_id)

@app.route('/count-tesla-primary', methods=['GET'])
def count_tesla_primary():
    primary_collection = collection.with_options(read_preference=ReadPreference.PRIMARY)
    count = primary_collection.count_documents({"Make": "TESLA"})
    return jsonify({"count": count})

@app.route('/count-bmw-secondary', methods=['GET'])
def count_bmw_secondary():
    secondary_collection = collection.with_options(read_preference=ReadPreference.SECONDARY_PREFERRED)
    count = secondary_collection.count_documents({"Make": "BMW"})
    return jsonify({"count": count})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
