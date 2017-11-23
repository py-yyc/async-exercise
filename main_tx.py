import time
import json

import treq

from twisted.internet.defer import Deferred, inlineCallbacks, ensureDeferred, DeferredList
from twisted.internet.task import react
from twisted.web.client import readBody


# This is the same as the code in the presentation; we will use "async
# def" and "await" throughout.


async def fetch(uri):
    response = await treq.get(
        uri,
        headers={
            b"User-Agent": [b"Twisted"],
        }
    )
    # download the reply
    raw_data = await readBody(response)
    return json.loads(raw_data)


async def main(reactor):
    # request all events for PyYYC's organization
    start = reactor.seconds()
    repos = await fetch(u'https://api.github.com/orgs/py-yyc/repos')
    if not isinstance(repos, list):
        print("bad: {}".format(repos))
        return 1

    # ... process data. Here we want to:
    # 1. parse the data base JSON (should return a list-of-dicts)
    # 2. sort by "updated_at"
    # 3. list the most-recent 5 repositories

    def sort_created(repo):
        return time.strptime(
            repo["updated_at"],
            "%Y-%m-%dT%H:%M:%SZ", # "2014-02-28T11:48:55Z"
        )

    repositories = list(
        reversed(
            sorted(repos, key=sort_created)
        )
    )[:5]

    if False:
        all_commits = []
        for repo in repositories:
            url = u"https://api.github.com/repos/py-yyc/{}/commits".format(repo["name"])
            all_commits.append(fetch(url))
        all_commits = await DeferredList([ensureDeferred(d) for d in all_commits])
        print("hi {}".format(len(all_commits)))
        all_commits = [result[1] for result in all_commits]
    else:
        all_commits = []
        for repo in repositories:
            url = u"https://api.github.com/repos/py-yyc/{}/commits".format(repo["name"])
            data = await(fetch(url))
            all_commits.append(data)

    for repo, commits in zip(repositories, all_commits):
        print(type(repo))
        print("{name} ({updated_at}): {latest_commit}".format(latest_commit=commits['sha'], **repo))

    diff = reactor.seconds() - start
    print("Took {}s".format(diff))


if __name__ == '__main__':
    react(lambda r: ensureDeferred(main(r)))

# correct output:
# py-yyc.github.com (2017-09-28T23:28:51Z): d21812048cae086ee37ee59c918e5c1055930a5c
# python-time-and-timezones (2017-09-28T19:19:11Z): 9429b5210c3c6844b3d797bc1d0c0a65561d1146
# pytest-selenium (2017-08-29T05:33:00Z): bd16acd9dcc7cc862c35b2fc3903b5bdd3c98e5d
# async-code (2017-06-27T16:54:40Z): aa9e0bc9c50fcd3a22fc770d7a60d0cf5f459605
# slackbot (2017-03-29T01:27:59Z): f6e7459d0f232ddfaa9f7fea266cdaa77f415678
