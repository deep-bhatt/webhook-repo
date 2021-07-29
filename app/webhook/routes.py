from flask import Blueprint, json, request, render_template
from dateutil import parser
from ..extensions import mongo

webhook = Blueprint(
    "Webhook", __name__, url_prefix="/webhook", template_folder="templates"
)


# im pretty sure there is an elegant way of doing this
# instead of making individual routes for 'push', 'merge'... etc
@webhook.route("/receiver/push", methods=["POST"])
def receiver_push():
    _json = request.json
    request_id = _json["after"]
    author = _json["pusher"]["name"]
    action = "PUSH"
    from_branch = _json["ref"].split("/")[-1]
    to_branch = _json["ref"].split("/")[-1]
    timestamp = _json["head_commit"]["timestamp"]
    timestamp = parser.parse(timestamp)

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

    return {"success": True, "message": "push request inserted"}, 200


@webhook.route("/receiver/pull_request", methods=["POST"])
def receiver():
    _json = request.json
    request_id = _json["pull_request"]["id"]
    author = _json["pull_request"]["user"]["login"]
    action = "PULL_REQUEST"
    from_branch = _json["pull_request"]["head"]["ref"]
    to_branch = _json["pull_request"]["base"]["ref"]
    timestamp = _json["pull_request"]["created_at"]
    timestamp = parser.parse(timestamp)

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

    return {"success": True, "message": "pull request inserted"}, 200


@webhook.route("/display", methods=["GET"])
def display():
    return render_template("index.html")


@webhook.route("/fetch", methods=["GET"])
def fetch():
    # in json
    results = list(mongo.db.requests.find({}, {"_id": 0}))
    for r in results:
        time_label = r["timestamp"].strftime("%d %B %Y - %I:%M %p")
        time_label += " " + "UTC"
        r["time_label"] = time_label
        print(r)
    return json.dumps(results)
