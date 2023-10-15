import sys
from gunicorn.app.wsgiapp import run
if __name__ == '__main__':
    sys.argv = "gunicorn --bind 0.0.0.0:5151 --reload --threads 4 --timeout 600 app:app".split()
    sys.exit(run())