from flask import Flask, request, jsonify

app = Flask(__name__)
rooms = {}  # { room_id: {"relay_ip": str, "players": int, "max_players": int} }

@app.route("/")
def index():
    return "FishNet Master Server is running!"

@app.route("/create", methods=["POST"])
def create():
    data = request.get_json()
    room_id = data["room_id"]
    relay_ip = data["relay_ip"]
    rooms[room_id] = {
        "relay_ip": relay_ip,
        "players": 0,
        "max_players": 2  # 任意
    }
    return jsonify({"ok": True, "room_id": room_id})

@app.route("/join/<room_id>", methods=["GET"])
def join(room_id):
    if room_id in rooms:
        room = rooms[room_id]
        if room["players"] < room["max_players"]:
            room["players"] += 1
            return jsonify({"relay_ip": room["relay_ip"], "players": room["players"]})
        else:
            return jsonify({"error": "Room full"}), 403
    else:
        return jsonify({"error": "Room not found"}), 404

@app.route("/leave/<room_id>", methods=["POST"])
def leave(room_id):
    if room_id in rooms:
        rooms[room_id]["players"] = max(0, rooms[room_id]["players"] - 1)
        return jsonify({"ok": True, "players": rooms[room_id]["players"]})
    else:
        return jsonify({"error": "Room not found"}), 404
