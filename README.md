To run locally
===

Dependencies
---

Python virtualenv (`sudo pip install virtualenv` once you have pip. Get pip with `sudo easy_install pip` if you don't have it.)

Create the virtual env
---

    virtualenv --no-site-packages env


Activate the virtual env
---
You have to do this in your shell every time you want to run the server.

    source env/bin/activate

Install dependencies
---
    pip install -r requirements.txt


Run the server
---
    FLASK_APP=app.py FLASK_DEBUG=1 flask run
