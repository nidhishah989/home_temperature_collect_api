# using elephantsql api created a postgresql on AWS services
import os
import psycopg2 #POSTgreSQL database adapter 
from datetime import datetime,timezone
from flask import Flask,request
from dotenv import load_dotenv # Read key-value pairs from a .env file and set them as environment variables

load_dotenv()

app = Flask(__name__)
db_url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(db_url) # connect with database

@app.get("/")
def home():
    with connection:
        with connection.cursor() as cur:
            rooms_table_creation="CREATE TABLE IF NOT EXISTS rooms (roomid SERIAL PRIMARY KEY, rname TEXT);"
            cur.execute(rooms_table_creation)
            temp_table_creation ="""CREATE TABLE IF NOT EXISTS temperatures (id SERIAL PRIMARY KEY, room_id INTEGER, temperature REAL, 
                                    date TIMESTAMP, FOREIGN KEY(room_id) REFERENCES rooms(roomid) ON DELETE CASCADE);"""
            cur.execute(temp_table_creation)
    return "Welcome to temperature collector app."

@app.post("/api/room")
def create_room():
    data = request.get_json()
    room_name = data["roomname"]
    with connection:
        with connection.cursor() as cur:
            room_creation_query = "INSERT INTO rooms (rname) VALUES (%s) RETURNING roomid;"
            cur.execute(room_creation_query,(room_name,))
            room_id = cur.fetchone()[0]
    return {"id":room_id, "message":f"Room {room_name} created."},201

@app.post("/api/temp")
def add_room_temperature():
    data = request.get_json()
    room_id = data["roomid"]
    temperature = data["temperature"]
    try:
        date = datetime.strptime(data ["date"],"%m-%d-%Y %H:%M:%S")
    except KeyError:
        date = datetime.now(timezone.utc)
    
    with connection:
        with connection.cursor() as cur:
            insert_temp_data= "INSERT INTO temperatures (room_id, temperature, date) VALUES (%s, %s, %s);"
            cur.execute(insert_temp_data,(room_id,temperature,date))
    return {"message": "Temperature added."},201

@app.get("/api/room/<int:room_id>")
def get_room_temperatures(room_id):
    
    with connection:
        
        with connection.cursor() as cur:
            getroomname = "SELECT rname FROM rooms WHERE roomid = (%s);"
            getalldataofroom = "SELECT * FROM temperatures WHERE room_id = (%s);"
            cur.execute(getroomname,(room_id,))
            roomname = cur.fetchone()[0]
            cur.execute(getalldataofroom,(room_id,))
            room_temperatures = cur.fetchall()
    return { "room name":roomname, "temperature_Data":room_temperatures}
