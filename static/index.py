from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
import re
import os.path

class IndexPage(webapp.RequestHandler):

    def get(self):
        self.redirect("calibration.html")

application = webapp.WSGIApplication(
                                     [('/', IndexPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
