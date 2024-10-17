import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False  
CORS(app)

jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)



@app.route('/members', methods=['GET'])
def get_all_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200 
    except Exception as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500



@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        
        if member:
            return jsonify(member), 200
        else:
            return jsonify({"error": "Member not found"}), 404
    except Exception as e:
        return jsonify({"error": "Server error", "message": str(e)}), 500



@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()

    if not all(key in data for key in ("id", "first_name", "age", "lucky_numbers")):
        return jsonify({"error": "Missing fields"}), 400


    new_member = {
        "id": data["id"],  
        "first_name": data["first_name"],
        "last_name": jackson_family.last_name,
        "age": data["age"],
        "lucky_numbers": data["lucky_numbers"]
    }

    if any(member['id'] == new_member['id'] for member in jackson_family.get_all_members()):
        return jsonify({"error": "ID already exists"}), 400

    jackson_family.add_member(new_member)

    return jsonify(new_member), 200



@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    except ValueError:
        return jsonify({"error": "Member not found"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
