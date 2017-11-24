import asyncio
import json

import aiohttp

# Get api from config file
with open("api-key.json") as config_file:
    json_data = json.load(config_file)
    githubAccessKey = json_data["api"]

def generateAuthenticatedGithubUrl(url):
    return "{}?access_token={}".format(url, githubAccessKey)


# Async fetch data from url. Returns raw response
async def fetchFromUrl(url, append_access_token=True):
    if append_access_token:
        url = generateAuthenticatedGithubUrl(url)

    print("Fetching {}".format(url))

    async with aiohttp.ClientSession(loop=loop) as session:
        req_context = session.get(
            url,
            headers={
                u"User-Agent": u"asyncio",
            }
        )
        async with req_context as response:
            raw_data = await response.text()
    print("Received {} bytes".format(len(raw_data)))
    return raw_data


async def main(loop):
    # download from a URL
    repos_raw = await fetchFromUrl("https://api.github.com/orgs/py-yyc/repos")

    # ... process data. Here we want to:
    # 1. parse the data from JSON (should return a list-of-dicts)
    json_data = json.loads(repos_raw)
    # 2. sort by "updated_at"
    sorted_repos_data = sorted(json_data, key=lambda k: k['updated_at'], reverse=True)
    # 3. list the most-recent 5 repositories
    # 4. for each repo ^ make a new URI to fetch commits
    # 5. fetch URI, determine SHA of most-recent commit
    for c, repo in enumerate(sorted_repos_data[:5]):
        print("starting " + str(c))
        repo_raw = await fetchFromUrl(repo['url'] + "/commits")
        json_repo = json.loads(repo_raw)
        print("{} -- {}".format(repo['name'], json_repo[0]['sha']))
        print("ending " + str(c))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
