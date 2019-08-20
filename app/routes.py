import logging

import flask
from flask import Response, request, jsonify

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)

@app.route("/profile", methods=["GET"])
def profile():
    github_username = request.args.get("github")
    bitbucket_username = request.args.get("bitbucket")
    # feature add: handle only one is supplied
    if github_username is None: 
        return Response("Missing github profile", status=400)
    if bitbucket_username is None:
        return Response("Missing bitbucket profile", status=400)
    else:
        return jsonify({"github": github_username, "bitbucket": bitbucket_username})




''' test:
hit /profile
expect 400 with message: missing gihub profile

hit /profile?bitbucket=abc
expect 400 with message: missing gihub profile

hit /profile?github=abc
expect 400 with message: missing bitbucket profile

hit /profile?github=abc&bitbucket=def
expect 200 with json of github and bitbucket
'''
