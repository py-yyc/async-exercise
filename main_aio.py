import asyncio
import json

import aiohttp

# Get api from config file
with open("api-key.json") as config_file:
    githubAccessKey = json.load(config_file)["api"]


def generateAuthenticatedGithubUrl(url):
    return "{}?access_token={}".format(url, githubAccessKey)


# Async fetch data from url. Returns raw response
async def fetchFromUrl(url, append_access_token=True, verbose=False):
    if append_access_token:
        url = generateAuthenticatedGithubUrl(url)

    if verbose:
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
    if verbose:
        print("Received {} bytes".format(len(raw_data)))
    return raw_data


# receive a dictionary that contains a 'url' and 'name'
async def fetch_repo_data(url, name):
    repo_raw = await fetchFromUrl(url)
    json_repo = json.loads(repo_raw)
    print("{} -- {}".format(name, json_repo[0]['sha']))


async def main(loop):
    # download from a URL
    repos_raw = await fetchFromUrl("https://api.github.com/orgs/py-yyc/repos")

    # ... process data. Here we want to:
    # 1. parse the data from JSON (should return a list-of-dicts)
    json_data = json.loads(repos_raw)

    # 2. sort by "updated_at"
    sorted_repos_data = sorted(json_data, key=lambda k: k['updated_at'], reverse=True)

    # 3. list the most-recent 5 repositories
    print("--------\n5 most recent repos:")
    # 4. for each repo ^ make a new URI to fetch commits
    # 5. fetch URI, determine SHA of most-recent commit
    awaits = []
    for c, repo in enumerate(sorted_repos_data[:5]):
        print("{}) {} -- {}".format(str(c + 1), repo['name'], repo['updated_at']))
        awaits.append(fetch_repo_data(repo['url'] + "/commits", repo['name']))

    print("--------\nMost recent SHA:")
    await asyncio.wait(awaits)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
