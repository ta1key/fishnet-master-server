
from flask import Flask, request, jsonify

app = Flask(__name__)
rooms = {}

@app.route("/")
def index():
    return "FishNet Master Server is running!"

@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    room_id = data["room_id"]
    relay_ip = data["relay_ip"]
    rooms[room_id] = relay_ip
    return jsonify({"ok": True, "room_id": room_id})

@app.route("/join/<room_id>", methods=["GET"])
def join(room_id):
    if room_id in rooms:
        return jsonify({"relay_ip": rooms[room_id]})
    else:
        return jsonify({"error": "Room not found"}), 404