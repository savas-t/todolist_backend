import uuid
from flask import Flask, request, jsonify, abort

# Initialize Flask server
app = Flask(__name__)

# Define internal data structures
lists = []
entries = []


# Add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, PUT"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"

    return response


## HELPER FUNCTIONS ##


# Returns list with given id, returns None if no list was found
def get_list(list_id):
    for list in lists:
        if list["id"] == list_id:
            return list

    return None


# Returns entry with given id, returns None if no entry was found
def get_entry(entry_id):
    for entry in entries:
        if entry["id"] == entry_id:
            return entry

    return None


## ENDPOINTS ##


# Add new list to lists
@app.route("/todo-list", methods=["POST"])
def add_list():
    # Format json from request body to a dictionary
    request_data = request.get_json(force=True)

    # Check if required parameter is missing
    if "name" not in request_data.keys():
        return "Request parameter 'name' is missing.", 400

    # Create a new list
    new_list = {"id": str(uuid.uuid4()), "name": request_data["name"]}

    # Add new list to lists
    lists.append(new_list)

    return jsonify(new_list), 200


# Show or delete list
@app.route("/todo-list/<list_id>", methods=["GET", "DELETE"])
def handle_list(list_id):
    # Find list of according list id
    list = get_list(list_id)

    # If list is None, there is no list with given id
    if list == None:
        return 'There is no list with id "' + list_id + '"', 404

    # Handle GET request & show list entries
    if request.method == "GET":
        return jsonify([entry for entry in entries if entry["list_id"] == list_id])

    # Handle DELETE request & delete list with given id
    if request.method == "POST":
        lists.remove(list)

        return "", 200


# Add new entry to list
@app.route("/todo-list/<list_id>/entry", methods=["POST"])
def add_entry(list_id):
    # Find list of according list id
    list = get_list(list_id)

    # If list is None, there is no list with given id
    if list == None:
        return 'There is no list with id "' + list_id + '"', 404

    # Grab request data
    request_data = request.get_json(force=True)

    # Check if parameters are missing
    if "name" not in request_data.keys():
        return "Request parameter 'name' is missing.", 400

    if "beschreibung" not in request_data.keys():
        return "Request parameter 'beschreibung' is missing.", 400

    # Create a new entry dictionary
    new_entry = {
        "id": str(uuid.uuid4()),
        "list_id": list["id"],
        "name": request_data["name"],
        "beschreibung": request_data["beschreibung"],
    }

    # Add new entry to entries
    entries.append(new_entry)

    return "", 200


# Update or delete an entry
@app.route("/todo-list/<list_id>/entry/<entry_id>", methods=["PUT", "DELETE"])
def handle_entry(list_id, entry_id):
    # Find list of according list id
    list = get_list(list_id)

    # If list is None, there is no list with given id
    if list == None:
        return 'There is no list with id "' + list_id + '"', 404

    # Find entry of according entry id
    entry = get_entry(entry_id)

    # If entry is None, there is no entry with given id
    if entry == None:
        return 'There is no entry with id "' + entry_id + '"', 404

    # Grab request data
    request_data = request.get_json(force=True)

    # Handle PUT request & update entry
    if request.method == "PUT":
        key_exists = False

        for key in request_data.keys():
            if key in entry.keys():
                key_exists = True
                entry[key] = request_data[key]

        if key_exists == False:
            return "There is no entry key which matches your keys", 400

    # Handle DELETE request & delete entry
    if request.method == "DELETE":
        entries.remove(entry)

    return "", 200


if __name__ == "__main__":
    # start Flask server
    app.debug = True
    app.run(host="0.0.0.0", port=5000, debug=True)
