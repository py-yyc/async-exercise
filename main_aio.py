import time
import json

import asyncio
import aiohttp

async def fetch(url):
    with aiohttp.ClientSession(loop=loop) as session:
        req_context = session.get(
            url,
            headers={
                u"User-Agent": u"asyncio",
            }
        )
        async with req_context as response:
            text = await response.text()
            print(f"{url} ready")
            return {"url": url, "object": json.loads(text)}

def repos_url():
    return u"https://raw.githubusercontent.com/py-yyc/async-exercise/master/data/repos.json"

def repo_data_url(repo_name):
    return f"https://raw.githubusercontent.com/py-yyc/async-exercise/master/data/{repo_name}_commits.json"

class AwaitList:
    def __init__(self, l):
        self.waiting = set()
        self.ready = []
        self.ready_signal = asyncio.Event()

        for item in l:
            future = asyncio.ensure_future(item)
            self.waiting.add(future)
            future.add_done_callback(self._done)

    def _done(self, future):
        self.waiting.remove(future)
        self.ready.append(future.result())
        self.ready_signal.set()

    def __aiter__(self):
        return self

    async def __anext__(self):
        while len(self.ready) != 0 or len(self.waiting) != 0:
            if len(self.ready) > 0:
                item = self.ready.pop(0)
                return item
            if len(self.waiting) > 0:
                await self.ready_signal.wait()
                self.ready_signal.clear()
        raise StopAsyncIteration()

async def main(loop):
    repos = (await fetch(repos_url()))["object"]
    repos.sort(key=lambda x: x["updated_at"])

    async for x in AwaitList(
            fetch(repo_data_url(repo['name']))
            for repo in repos[-5:]):
        print("done with", x["url"], len(x["object"]))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
