import unittest
import json
from app.routes import getNextGithubUrl, addInfoFromGithubProfile
from requests.structures import CaseInsensitiveDict
from collections import defaultdict


SERVERLESS_PROFILE = json.loads('''
{
  "languages": {
    "JavaScript": 57,
    "Python": 1,
    "Shell": 1,
    "unspecified": 7,
    "CSS": 2,
    "Go": 5,
    "Dockerfile": 1,
    "TypeScript": 1
  },
  "num_repos_forked": 4,
  "num_repos_original": 71,
  "num_repos_total": 75,
  "num_repos_unspecified": 0,
  "watchers": 47531,
  "topics": {
    "aws": 3,
    "aws-lambda": 5,
    "azure-functions": 3,
    "blog": 1,
    "examples": 1,
    "github-actions": 1,
    "google": 1,
    "google-cloud": 1,
    "google-cloud-functions": 4,
    "guide": 1,
    "ibm-cloud-functions": 1,
    "ibm-openwhisk": 1,
    "javascript": 1,
    "microservice": 1,
    "openwhisk": 1,
    "serverless": 23,
    "serverless-applications": 2,
    "serverless-architectures": 3,
    "serverless-components": 1,
    "serverless-framework": 14,
    "serverless-functions": 1,
    "serverless-plugin": 2,
    "serverless-providers": 1,
    "stdlib": 1,
    "meetups": 1,
    "phenomic": 1,
    "presentations": 1,
    "pubsub": 1,
    "scheduler": 1,
    "sdk-js": 1,
    "sdk-nodejs": 1,
    "serverless-offline": 1,
    "speakers": 1,
    "static-site-generator": 1,
    "usergroups": 1,
    "utils": 1,
    "webhooks": 1,
    "api-gateway": 1,
    "azure": 1,
    "dataflow": 1,
    "dynamodb": 1,
    "event-driven": 1,
    "event-gateway": 3,
    "event-router": 1,
    "faas": 3,
    "faas-emulator": 1,
    "function-emulator": 1,
    "functions-as-a-service": 1,
    "gatsby": 1,
    "gcf": 1,
    "github": 1,
    "golang": 1,
    "hexo": 1,
    "hugo": 1,
    "jekyll": 1,
    "lambda": 1
  }   
}
''')

class TestAPIMethods(unittest.TestCase):

    def test_get_next_none(self):
        headers = CaseInsensitiveDict({"Link": '<https://api.github.com/organizations/13742415/repos?page=2>; rel="prev", <https://api.github.com/organizations/13742415/repos?page=1>; rel="first"'})
        self.assertIsNone(getNextGithubUrl(headers))

    def test_get_next_present(self):
        headers = CaseInsensitiveDict({"Link": '<https://api.github.com/organizations/13742415/repos?page=1>; rel="prev", <https://api.github.com/organizations/13742415/repos?page=3>; rel="next", <https://api.github.com/organizations/13742415/repos?page=3>; rel="last", <https://api.github.com/organizations/13742415/repos?page=1>; rel="first"'})
        self.assertEqual(getNextGithubUrl(headers), 'https://api.github.com/organizations/13742415/repos?page=3')

    def test_get_profile(self):
        self.assertEqual(SERVERLESS_PROFILE["num_repos_original"], 71)
        ret = {}
        ret['num_repos_original'] = 0
        ret['num_repos_forked'] = 0
        ret['num_repos_unspecified'] = 0
        ret['num_repos_total'] = 0
        languages = defaultdict(lambda: 0)
        topics = defaultdict(lambda: 0)
        ret['watchers'] = 0
        addInfoFromGithubProfile("serverless", ret, languages, topics)
        print(ret)
        self.assertEqual(ret, SERVERLESS_PROFILE)


if __name__ == '__main__':
    pass # test not up to date, included for reference, see README
    #unittest.main() 
