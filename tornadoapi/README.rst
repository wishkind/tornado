lateral-tornado-api
=============================

About
-------------

This is a simple example of using asyncio event loop with tornado to create a REST application.

This returns news stories from Lateral Endpoint and send response to FE.


Async tests are also written using asyncio event loop.

Install
-------

In order to run this, you need to install python 3.6 for asyncio with async/await. Python 3.5 might not work.

Install dependencies with `pip install -r requirements.txt`.

Usage
-----

You can run the app with `python main.py`.

Then in browser url enter `localhost:8080`.

Tests can be run with `python -m tornado.testing tests/tests.py`


