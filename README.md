
# Coding Challenge App

Implemented by Michael Lipman
August 20, 2019

## Install:
Create and activate virtualenv for python3 and pip3

Then pip install from the requirements file
``` 
pip install -r requirements.txt
```

## Running the code

### Spin up the service

```
# start up local server
python -m run 
```

### Making Requests
Server runs on port 5000.
The url for a profile is `/profile` and it expects query params of github and bitbucket.
```
curl -i "http://127.0.0.1:5000/profile?github=serverless&bitbucket=serverless"
```


## What'd I'd like to improve on...

### Missing Data
I was able to get all the fields from the github api. But for the bitbucket api, I wasn't able to get whether it was a fork or topics or a watcher count. So for repo counts there is a total, and then counts for forked, original, and unspecified.

### Testing
I used some unittests to write the code and I've included the file for reference, but I would like to have a full set of up to date tests for all the methods. Also, a big part of that would be mocks of server responses. When writing a test, I used a watcher count for a popular repo. Then a bit later when running it, the watcher count had updated, so the test failed. This could be fixed by having the test reference a mock api response. However, in development, generating those api responses, especially with pagination, was often the thing being worked on, so using a mock would not have helped that stage.

### Error handling and Inference

I would like it to handle more edge and error cases. If bitbucket is provided but github is not or github is provided and bitbucket is not, it should fetch a single profile. If a single organization name is provided, it should see if it works for either or both and return what it can find. It should also give more informative error messages when the api throws an error.

### Authentication
A proper API would handle authentication and deal with getting proper tokens before making calls

### Pagination
This synchronously goes through each page until it ends, but that could be dozens or more api calls before it returns. Long running processes are not best served by synchronous HTTP responses, but there is complexity in setting up a different system. One way would be for the profile API to return a job id, then the client can poll that job id and when the job is done, it will get back the full profile.

### Combining Duplicates
I did not combine repos from different sources, but conceivably you could. You could do so simply by comparing names, or get more in depth by looking at attributes of the repo like commits or languages, though that would probably require more api calls.