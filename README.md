# Secondary Structure Prediction Display - Browser Version
An application that sends a protein sequence to various websites to generate predictions. The results are then scraped and saved into a database that is accessed for display.

Setting Up
-----------
This application requires a token.pickle and credentials.json in the services folder. 

**credentials.json** can be made by creating a project on the [Google Cloud Platform](https://console.cloud.google.com/). This application only uses the Gmail API.

**token.pickle** can be created by running the createPickle function found in services/emailtools.py and logging into a Google account.

A database is required to run this application. The url can be set in app.py with the `DATABASE_URL` variable.

If hosting this application on Heroku, run the command `heroku config:set WEB_CONCURRENCY=1` to make the Running Counter accurate.

Dependencies
-----------
```
beautifulsoup4 lxml urllib3 Flask gevent-websocket wtforms Flask-WTF psycopg2-binary --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib python-guerrillamail
```