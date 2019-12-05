# Secondary Structure Prediction Display - Browser Version
An application that sends a protein sequence to various websites to generate predictions. The results are then scraped and saved into a database that is accessed for display.

Dependencies
-----------
```bash
beautifulsoup4 lxml urllib3 Flask gevent-websocket wtforms Flask-WTF psycopg2-binary --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib python-guerrillamail
```