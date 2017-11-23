PyYYC: Async Web Client
=======================

This is a skeleton for a programming assignment to explore an
asynchronous Web client written using Twisted or asyncio.

Must use Python3.

Getting Started
---------------

To create a virtualenv and install all requirements:

    python3 -m venv venv3
    source venv3/bin/activate
    python3 -m pip install -r requirements.txt

This will install both treq and aiohttp.

Start with either `main_tx.py` or `main_aio.py` depending upon whether
you want to use Twisted or asyncio (if you finish, try the other
framework).


The Assignment
--------------

1. List all py-yyc repos

  - url: https://api.github.com/orgs/py-yyc/repos
  - bonus: list the 5 most recent (newest to oldest)

2. discover the SHA1 of the most-recent commit of each repo

 - url: https://api.github.com/repos/py-yyc/{repo}/commits
 - bonus: retrieve these in parallel

3. bonus: use authentication


Note: without logging in, it's possible we'll hit the rate-limits. If
that happens, you can use these URIs instead:


