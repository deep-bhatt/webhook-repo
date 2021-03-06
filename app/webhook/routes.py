from flask import Blueprint, json, request, render_template
from dateutil import parser
from ..extensions import mongo

webhook = Blueprint(
    "Webhook", __name__, url_prefix="/webhook", template_folder="templates"
)


@webhook.route("/display", methods=["GET"])
def display():
    return render_template("index.html")


@webhook.route("/receiver", methods=["POST"])
def receiver_merge():
    _json = request.json

    # push request
    if "before" and "after" in _json:
        request_id = _json["after"]
        author = _json["pusher"]["name"]
        action = "PUSH"
        from_branch = to_branch = _json["ref"].split("/")[-1]
        timestamp = _json["head_commit"]["timestamp"]
        timestamp = parser.parse(timestamp)
    elif "pull_request" in _json:
        pull_request = _json["pull_request"]

        if _json["action"] == "opened":
            action = "PULL_REQUEST"
            timestamp = pull_request["created_at"]
        elif _json["action"] == "closed":
            action = "MERGE"
            timestamp = pull_request["merged_at"]

        request_id = pull_request["id"]
        author = pull_request["user"]["login"]
        from_branch = pull_request["head"]["ref"]
        to_branch = pull_request["base"]["ref"]
        timestamp = parser.parse(timestamp)
    else:
        return "Not Yet Implemented", 404

    # print(request_id, author, action, from_branch, to_branch, timestamp)

    id = mongo.db.requests.insert(
        {
            "request_id": request_id,
            "author": author,
            "action": action,
            "from_branch": from_branch,
            "to_branch": to_branch,
            "timestamp": timestamp,
        }
    )

    return {"success": True, "message": "record inserted"}, 200


@webhook.route("/fetch", methods=["GET"])
def fetch():
    results = list(mongo.db.requests.find({}, {"_id": 0}))
    for r in results:
        time_label = r["timestamp"].strftime("%d %B %Y - %I:%M %p")

        # time is stored as UTC in MongoDB
        time_label += " " + "UTC"
        r["time_label"] = time_label
        print(r)
    return json.dumps(results)
