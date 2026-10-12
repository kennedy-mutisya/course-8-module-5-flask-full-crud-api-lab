
from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data model
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


# In-memory database
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# Welcome route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the Event Management API"
    }), 200


# GET /events - Retrieve all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([event.to_dict() for event in events]), 200


# POST /events - Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    # Validate the request body
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A valid title is required"}), 400

    # Generate a new unique ID
    new_id = max((event.id for event in events), default=0) + 1

    # Create and store the event
    new_event = Event(new_id, title.strip())
    events.append(new_event)

    # Return the created event with HTTP 201
    return jsonify(new_event.to_dict()), 201


# PATCH /events/<event_id> - Update an event's title
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    # Find the requested event
    event = next(
        (event for event in events if event.id == event_id),
        None
    )

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    title = data["title"]

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A valid title is required"}), 400

    # Update the existing event
    event.title = title.strip()

    return jsonify(event.to_dict()), 200


# DELETE /events/<event_id> - Remove an event

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    # Find the event by ID
    event = next(
        (event for event in events if event.id == event_id),
        None
    )

    # Return 404 if the event does not exist
    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Remove the event from the in-memory list
    events.remove(event)

    # Return 204 No Content after successful deletion
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
