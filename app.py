from flask import Flask, render_template, request, jsonify
import json
import os
import time
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

@app.route("/payload",  methods = ['POST'])
def payload():
    """
    GitHub's webhook listener function to add branch protection whenever a new repo is created under a org.
    Accepts GitHub's webhook request on creation of a new repo
    :return: "Done"
    """
    payload = request.get_json()

    # GitHub's username
    user = "VenkateshCTA"
    # GitHub's token & reading it from the env variable
    token = os.environ['token']
    try:
        if payload["action"] == "created":
            # Add delay for a sec or else we will get 404
            time.sleep(1)
            # Branch protection policy for the master branch
            branch_protection = {
                "required_status_checks": {"strict": True, "contexts": ["default"]},
                "enforce_admins": False,
                "required_pull_request_reviews": None,
                "restrictions": None
            }
            # Custom header mandatory or else you'll end up in error
            headers = {'Accept': 'application/vnd.github.luke-cage-preview+json'}
            # Branch protection PUT API call with Basic Auth
            branch_protection_response = requests.put(
                payload["repository"]["url"] + "/branches/master/protection", auth=HTTPBasicAuth(user, token),
                headers=headers, data=json.dumps(branch_protection))

            if branch_protection_response.status_code == 200:
                print("Branch protection added. Status: ", branch_protection_response.status_code)

                # Create issue in repo
                if payload["repository"]["has_issues"]:
                    issue = {
                        "title": "YAY!! Branch Protection got Added",
                        "body": "@" + user + ", Branch protection was added to the master branch."
                    }
                    # Issue creation POST API call with Basic Auth
                    issue_creation_response = requests.post(
                        payload["repository"]["url"] + "/issues",
                        auth=HTTPBasicAuth(user, token), data=json.dumps(issue))

                    if issue_creation_response.status_code == 201:
                        print("Issue creation success. Status: ", issue_creation_response.status_code)
                    else:
                        print("Unable to create issue. Status: ", issue_creation_response.status_code)

            else:
                print(branch_protection_response.content)
                print("Unable to create branch protection. Status: ", branch_protection_response.status_code)

    except KeyError:
        pass

    return "Done"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)