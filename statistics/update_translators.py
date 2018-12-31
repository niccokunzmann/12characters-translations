#!/usr/bin/python3 -u
import requests
import os
from pprint import pprint
from collections import defaultdict
import json

HERE = os.path.dirname(__file__) or "."
TOKEN = os.environ["TRANSIFEX_TOKEN"] # requires api token from transifex, see https://docs.transifex.com/api/introduction#authentication
AUTH = ("api", TOKEN)


# get the resources
# curl -i -L --user api:$TRANSIFEX_TOKEN -X GET https://api.transifex.com/organizations/12-characters/projects/12-characters-play/resources/
RESOURCES_URL = "https://api.transifex.com/organizations/12-characters/projects/{project}/resources/"
# get the languages
# curl -i -L --user api:$TRANSIFEX_TOKEN -X GET https://api.transifex.com/organizations/12-characters/projects/12-characters-play/
PROJECT_URL = "https://api.transifex.com/organizations/12-characters/projects/{project}/"
# get the user translating it for a language
# curl -i -L --user api:$TRANSIFEX_TOKEN -X GET https://www.transifex.com/api/2/project/12-characters-play/resource/07-better-to-be-hopeful-txt/translation/de/strings/?details
TRANSLATIONS_URL = "https://www.transifex.com/api/2/project/{project}/resource/{resource_slug}/translation/{language}/strings/?details"

def get(url):
    return requests.get(url.format(**globals()), auth=AUTH).json()

users = defaultdict(lambda: defaultdict(int)) # lang: user: count

projects = ["12-characters-play", "12-characters-book"]
for project in projects:
    resources = get(RESOURCES_URL)
    project_data = get(PROJECT_URL)
    languages = [language["code"] for language in project_data["languages"]]
    for resource in resources:
        for language in languages:
            resource_slug = resource["slug"]
            strings = get(TRANSLATIONS_URL)
            for string in strings:
                user = string["user"]
                users[language][user] += 1

path = os.path.join(HERE, "usernames_to_real_names.json")
with open(path) as file:
    name_resolution = json.load(file)

for language, translators in users.items():
    usernames = list(translators)
    usernames.sort(key=lambda username: translators[username], reverse=True)
    names = [name_resolution.get(username, username) for username in usernames if username]
    path = os.path.join(HERE, "translators", language + ".txt")
    content = ", ".join(names)
    with open(path, "w") as file:
        file.write(content)
    print(language, " -> ", content)

