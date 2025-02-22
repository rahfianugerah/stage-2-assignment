# Import library
from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from statistics import mean

app = Flask(__name__)

# MongoDB Atlas Configuration
client = MongoClient("<MongoDBClient>")
db = client['<YourDatabase>']         # Ganti dengan nama database 
collection = db['<YourColletion>']     # Ganti dengan nama collection 

# Route POST to insert sensor data into MongoDB
@app.route('/data', methods=['POST'])
def post_sensor_data():
    data = request.get_json()
    try:
        # Mengambil data dari JSON request
        temperature = float(data.get('temperature'))
        humidity = float(data.get('humidity'))
        timestamp_str = data.get('timestamp')
        
        # Konversi timestamp jika disediakan, atau gunakan waktu UTC saat ini
        if timestamp_str:
            timestamp = datetime.fromisoformat(timestamp_str)
        else:
            timestamp = datetime.utcnow()
        
        sensor_data = {
            'temperature': temperature,
            'humidity': humidity,
            'timestamp': timestamp
        }
        
        result = collection.insert_one(sensor_data)
        return jsonify({
            "message": "Data inserted successfully",
            "id": str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route GET for counting average temperature
@app.route('/sensor1/temperature/avg', methods=['GET'])
def avg_temperature():
    try:
        docs = list(collection.find())
        if not docs:
            return jsonify({"message": "No data found"}), 404
        
        temperatures = [doc['temperature'] for doc in docs if 'temperature' in doc]
        if not temperatures:
            return jsonify({"message": "No temperature data found"}), 404
        
        avg_temp = mean(temperatures)
        return jsonify({"average_temperature": avg_temp}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route GET for counting average humidity
@app.route('/sensor1/humidity/avg', methods=['GET'])
def avg_humidity():
    try:
        docs = list(collection.find())
        if not docs:
            return jsonify({"message": "No data found"}), 404
        
        humiditys = [doc['humidity'] for doc in docs if 'humidity' in doc]
        if not humiditys:
            return jsonify({"message": "No humidity data found"}), 404
        
        avg_humidity_val = mean(humiditys)
        return jsonify({"average_humidity": avg_humidity_val}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':

    # Run the server
    app.run(debug=True)