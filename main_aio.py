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
        l = list(l)
        self.l = l
        self.waiting = set(l)
        self.ready = []
        self.given_for_future = {}
        self.ready_signal = asyncio.Event()
        # self.remaining = len(l)
        for i in self.waiting:
            future = asyncio.ensure_future(i)
            self.given_for_future[future] = i
            future.add_done_callback(self._done)

    def _done(self, future):
        # print(f"future {future} is done")
        given = self.given_for_future[future]
        self.waiting.remove(given)
        self.ready.append(future.result())
        # self.remaining -= 1
        self.ready_signal.set()

    def __aiter__(self):
        return self

    async def __anext__(self):
        while len(self.ready) != 0 or len(self.waiting) != 0:
            if len(self.ready) > 0:
                # print("one thing is ready")
                item = self.ready.pop(0)
                return item
            if len(self.waiting) > 0:
                # print(f'nothing ready, waiting for {self.remaining} items')
                await self.ready_signal.wait()
                self.ready_signal.clear()
                # print('got something!')
        # print("done waiting for list")
        raise StopAsyncIteration()

async def main(loop):
    # download from a URL
    # raw_data = await fetch(u"https://meejah.ca")
    # print("Received {} bytes".format(len(raw_data)))

    repos = (await fetch(repos_url()))["object"]
    repos.sort(key=lambda x: x["updated_at"])

    # async for repo in AwaitList(
    async for x in AwaitList(
            fetch(repo_data_url(repo['name']))
            for repo in repos[-5:]):
        print("done with", x["url"], len(x["object"]))
        # print(repo['name'])
#
#     for repo in repos[-5:]:
#         print(repo['name'])
#         x =
#         to_await.append(x)
#     results = await asyncio.gather(*to_await)
#
# d = Deferred()
# d.add_callback(lambda: print('foo'))
# await d ← adds to end of callback list
# print 'done'

# f'foo'
# 'done'

# 'done'
# 'foo'

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
