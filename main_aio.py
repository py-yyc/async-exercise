import time
import json

import asyncio
import aiohttp


async def main(loop):
    # download from a URL
    url = u"https://meejah.ca"

    async with aiohttp.ClientSession(loop=loop) as session:
        req_context = session.get(url, headers={u"User-Agent": u"asyncio"})
        async with req_context as resp:
            raw_data = await resp.text()

    print("Received {} bytes".format(len(raw_data)))

    # ... process data. Here we want to:
    # 1. parse the data from JSON (should return a list-of-dicts)
    # 2. sort by "updated_at"
    # 3. list the most-recent 5 repositories
    # 4. for each repo ^ make a new URI to fetch commits
    # 5. fetch URI, determine SHA of most-recent commit


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
