from flask import Flask, request, render_template, jsonify
from datetime import datetime
import json
import mysql.connector

application = Flask(__name__)

data_points = []

DB_CONFIG = {
    "host": "",  
    "user": "flaskuser",  
    "password": "", 
    "database": "iot"
}

def save_to_db(data):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = query = """
        INSERT INTO sensor_data (temperature, humidity, measurement, sensor_id)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (data["t"], data["h"], data["m"], data["i"]))
        connection.commit()
        cursor.close()
        connection.close()
        print("[INFO] Data successfully saved to MariaDB")
    except Exception as e:
        print("[ERROR] Failed to save data to MariaDB:", e)

@application.route("/")
def index():
    return render_template("index.html")

@application.route('/receive', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            data = json.loads(data)

        if not all(k in data for k in ("t", "h", "m", "i")):
            return jsonify({"error": "Invalid data format"}), 400

        record = {
            "t": data["t"],
            "h": data["h"],
            "m": data["m"],
            "i": data["i"],
            "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        data_points.append(record)

        print(f"[DATA] T:{record['t']} H:{record['h']} M:{record['m']} I:{record['i']}")

        return jsonify({"message": "Data received and saved successfully"})

    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        print("[ERROR]", e)
        return jsonify({"error": str(e)}), 500

@application.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_points)

@application.route('/query_data', methods=['GET'])
def query_data():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, temperature, humidity, measurement, sensor_id, created_at FROM sensor_data ORDER BY created_at DESC")
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template("query_data.html", rows=rows)
    except Exception as e:
        print("[ERROR] Failed to query data:", e)
        return f"<h3>Error al consultar datos: {e}</h3>", 500

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=8080)
