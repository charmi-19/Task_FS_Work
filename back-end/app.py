import json
from flask import Flask
from flask_cors import CORS
import pymysql
from pymysql.cursors import DictCursor

app = Flask("app")
CORS(app)

MYSQL_DB_USER = "YOUR_DB_USER"
MYSQL_DB_HOST = "YOUR_DB_HOST"
MYSQL_DB_PASSWORD = "YOUR_DB_PASSWORD"
MYSQL_DB = "YOUR_DB_NAME"


def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def mysql_connection():
    try:
        conn = pymysql.connect(
            host=MYSQL_DB_HOST,
            user=MYSQL_DB_USER,
            password=MYSQL_DB_PASSWORD,
            database=MYSQL_DB,
            cursorclass=DictCursor
        )
        return conn
    except pymysql.err.Error as err:
        print("Error connecting to MySQL:", err)
        return None

# API endpoint to push json file data into database
@app.route("/add/data", methods=['POST'])
def add_data_db():
    data = read_json('./data.json')
    connection = mysql_connection()
    cursor = connection.cursor()

    params = []
    for record in data:
        if "_id" in record and 'timestamp' in record:
            params.append({
                "id": record['_id']['$oid'],
                "timestamp": record['timestamp']['$date']['$numberLong'],
                "data": json.dumps(record)
            })

    query = "INSERT INTO human_data(id, timestamp, data) values(%(id)s, %(timestamp)s, %(data)s)"
    cursor.executemany(query, params)
    connection.commit()
    cursor.close()
    connection.close()
    return {"ok": True}

# Get API to retrieve stats
@app.route("/get/stats", methods=['GET'])
def get_data():
    connection = mysql_connection()
    cursor = connection.cursor()
    query = "SELECT id, timestamp, data from human_data order by id limit 50;"
    cursor.execute(query)
    data = cursor.fetchall()

    return {
        "ok": True,
        "result": [{
            "id": record["id"],
            "data": json.loads(record['data']),
            "timestamp": record['timestamp']
        } for record in data]
    }


if __name__ == "__main__":
    app.run(port=5050)
