import time
import json

import treq

from twisted.internet.defer import Deferred, inlineCallbacks, ensureDeferred, DeferredList
from twisted.internet.task import react
from twisted.web.client import readBody


# This is the same as the code in the presentation; we will use "async
# def" and "await" throughout.


async def main(reactor):
    # request all events for PyYYC's organization
    uri = u"https://meejah.ca"
    response = await treq.get(
        uri,
        headers={
            b"User-Agent": [b"Twisted"],
        }
    )
    # download the reply
    raw_data = await readBody(response)
    print("Received {} bytes".format(len(raw_data)))

    # ... process data. Here we want to:
    # 1. parse the data from JSON (should return a list-of-dicts)
    # 2. sort by "updated_at"
    # 3. list the most-recent 5 repositories
    # 4. for each repo ^ make a new URI to fetch commits
    # 5. fetch URI, determine SHA of most-recent commit


if __name__ == '__main__':
    def _main(reactor):
        return ensureDeferred(main(reactor))
    react(_main)
