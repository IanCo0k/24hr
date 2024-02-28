from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app, methods=["GET", "POST"])

# Sample initial data
time_slots = [
    {"time": "March 14 - 9:00 PM", "signups": []},
    {"time": "March 14 - 10:00 PM", "signups": []},
    {"time": "March 14 - 11:00 PM", "signups": []},
    {"time": "March 15 - 12:00 AM", "signups": []},
    {"time": "March 15 - 1:00 AM", "signups": []},
    {"time": "March 15 - 2:00 AM", "signups": []},
    {"time": "March 15 - 3:00 AM", "signups": []},
    {"time": "March 15 - 4:00 AM", "signups": []},
    {"time": "March 15 - 5:00 AM", "signups": []},
    {"time": "March 15 - 6:00 AM", "signups": []},
    {"time": "March 15 - 7:00 AM", "signups": []},
    {"time": "March 15 - 8:00 AM", "signups": []},
    {"time": "March 15 - 9:00 AM", "signups": []},
    {"time": "March 15 - 10:00 AM", "signups": []},
    {"time": "March 15 - 11:00 AM", "signups": []},
    {"time": "March 15 - 12:00 PM", "signups": []},
    {"time": "March 15 - 1:00 PM", "signups": []},
    {"time": "March 15 - 2:00 PM", "signups": []},
    {"time": "March 15 - 3:00 PM", "signups": []},
    {"time": "March 15 - 4:00 PM", "signups": []},
    {"time": "March 15 - 5:00 PM", "signups": []},
    {"time": "March 15 - 6:00 PM", "signups": []},
    {"time": "March 15 - 7:00 PM", "signups": []},
    {"time": "March 15 - 8:00 PM", "signups": []},
]

# Create operation to handle sign-up data
@app.route('/sign-up', methods=['POST'])
def sign_up():
    data = request.json
    time_slot = data.get("timeSlot")
    name = data.get("name")
    group = data.get("group")

    if not all([time_slot, name, group]):
        return jsonify({"error": "Incomplete sign-up data"}), 400

    for slot in time_slots:
        if slot["time"] == time_slot:
            slot["signups"].append({"name": name, "group": group})
            return jsonify({"message": "Sign-up successful"}), 201

    return jsonify({"error": "Time slot not found"}), 404

# Endpoint to view all signups
@app.route('/signups', methods=['GET'])
def get_signups():
    return jsonify({"time_slots": time_slots}), 200

@app.route('/delete-signups/<string:name>', methods=['DELETE'])
def delete_signups_by_name(name):
    deleted = False
    for slot in time_slots:
        signups = slot["signups"]
        for signup in signups[:]:  # Iterate over a copy of the list to allow modification
            if signup["name"] == name:
                signups.remove(signup)
                deleted = True
                print(f"Deleted signup: {signup}")
    if deleted:
        print(f"All entries with name '{name}' deleted successfully")
        return jsonify({"message": f"All entries with name '{name}' deleted successfully"}), 200
    else:
        print(f"No entries found with name '{name}'")
        return jsonify({"error": f"No entries found with name '{name}'"}), 404

if __name__ == '__main__':
    app.run(debug=True)
