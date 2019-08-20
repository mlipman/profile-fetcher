import logging
import flask
import requests
from flask import Response, request, jsonify
from collections import defaultdict
import json

GITHUB_BASE = 'https://api.github.com'
COMBO_ACCEPT = 'application/vnd.github.v3+json, application/vnd.github.mercy-preview+json'
GITHUB_HEADERS = {'Accept': COMBO_ACCEPT}  # confines use to api v3 and included topics
BITBUCKET_BASE = 'https://api.bitbucket.com'

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)


class Profile():
    def __init__(self):
        self.num_repos_original = 0
        self.num_repos_forked = 0
        self.num_repos_unspecified = 0
        self.num_repos_total = 0
        self.languages = defaultdict(lambda: 0)  # acts as dict with all values initilized to 0
        self.topics = defaultdict(lambda: 0)
        self.watchers = 0

    def to_dict(self):
        return {
            "num_repos_original": self.num_repos_original,
            "num_repos_forked": self.num_repos_forked,
            "num_repos_unspecified": self.num_repos_unspecified,
            "num_repos_total": self.num_repos_total,
            "watchers": self.watchers,
            "languages": dict(self.languages),
            "topics": self.topics,
        }


class APIError(Exception):
    pass


def githubReposUrl(org_name):
    return '/orgs/{org_name}/repos?per_page=100'.format(org_name=org_name)


def bitbucketReposURL(org_name):
    return '/2.0/repositories/{org_name}'.format(org_name=org_name)


def getNextGithubUrl(headers):
    if "Link" not in headers:
        return None
    links = requests.utils.parse_header_links(headers["Link"])
    next_link = [x for x in links if x['rel'] == 'next']
    if next_link:
        return next_link[0]['url']
    return None


def addInfoForGithubPage(url, profile):
    ''' Gets one page of results from github api '''
    r = requests.get(
        url=url,
        headers=GITHUB_HEADERS
    )
    if (int(r.status_code) >= 400):
        raise APIError()
    next_url = getNextGithubUrl(r.headers)
    for repo in r.json():
        profile.num_repos_total += 1
        if repo["fork"]:
            profile.num_repos_forked += 1
        else:
            profile.num_repos_original += 1
        profile.watchers += repo["watchers_count"]
        language = repo['language'] if repo['language'] is not None else 'unspecified'
        profile.languages[language.lower()] += 1
        for topic in repo['topics']:
            profile.topics[topic] += 1
    return next_url


def addInfoFromGithubProfile(org_name, profile):
    ''' Called by main route, pages through results, updating profile as it goes '''
    url = GITHUB_BASE + githubReposUrl(org_name)
    while True:
        next_url = addInfoForGithubPage(url, profile)
        if next_url is None:
            break
        else:
            url = next_url


def addInfoForBitbucketPage(url, profile):
    ''' Gets one page of results from bitbucket api '''
    r = requests.get(url)
    if (int(r.status_code) >= 400):
        raise APIError()
    next_url = r.json().get('next')
    for repo in r.json()['values']:
        language = repo['language'] if repo['language'] else 'unspecified'
        profile.languages[language.lower()] += 1
        profile.num_repos_total += 1
        profile.num_repos_unspecified += 1
    return next_url


def addInfoFromBitbucketProfile(org_name, profile):
    ''' Called by main route, pages through results, updating profile as it goes '''
    url = BITBUCKET_BASE + bitbucketReposURL(org_name)
    while True:
        next_url = addInfoForBitbucketPage(url, profile)
        if next_url is None:
            break
        else:
            url = next_url


@app.route("/profile", methods=["GET"])
def profile():
    github_username = request.args.get("github")
    bitbucket_username = request.args.get("bitbucket")
    if github_username is None:
        return Response("Missing github profile", status=400)
    if bitbucket_username is None:
        return Response("Missing bitbucket profile", status=400)

    profile = Profile()
    try:
        addInfoFromGithubProfile(github_username, profile)
    except APIError:
        return Response("Could not access Github API", status=500)
    try:
        addInfoFromBitbucketProfile(bitbucket_username, profile)
    except APIError:
        return Response("Could not access Bitbucket API", status=500)

    return jsonify(profile.to_dict())
