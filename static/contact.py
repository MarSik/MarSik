# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import mail
import re
import os.path

class ContactPage(webapp.RequestHandler):
    cleanup_re = r"\{\{[^}]+\}\}"

    def process(self, templ, var = None):
        if var is None:
            var = dict()
        self.response.headers['Content-Type'] = 'text/html'
        path = os.path.join(os.path.dirname(__file__), 'templates', templ)
        self.response.out.write(template.render(path, var))

    def get(self):
        self.process("contact.html", {"error": ""})

    def post(self):
        sender = self.request.get("email")
        subject = self.request.get("subject")
        text = self.request.get("text")
        bot = self.request.get("nospam")
        soucet = self.request.get("soucet")
        error = False

        args = {}
        for k in self.request.arguments():
            args[k] = self.request.get(k)

        if bot:
            self.response.set_status(403)
            return

        args["error"] = []

        if soucet!="8":
            args["error"].append(u"Neprošli jste kontrolou proti spamu, opravte součet prosím. You have failed the spam bot test, flease fix the form.")
            error = 1

        if not mail.is_email_valid(sender):
            args["error"].append(u"Zadali jste neplatný email, zkontrolujte si ho prosím. You have used an invalid email address, please correct it.")
            error = 1

        if len(subject)<2:
            args["error"].append(u"Prosím vyplňte předmět. Please fill the subject field.")
            error = 1

        if len(text)<2:
            args["error"].append(u"Prosím vyplňte text Vašeho dotazu. Please fill the inquiry field.")
            error = 1

        args["error"] = "<br/>".join(args["error"])

        if error:
            self.process("contact.html", args)
            return

        try:
            mail.send_mail(sender=u"Kontaktní formulář <www@montik.net>",
                           to=u"Martin Sivák <info@marsik.org>",
                           reply_to=sender,
                           subject=u"[info] "+subject,
                           body=text)
        except mail.Error, e:
            args["error"] = str(e)
            self.process("contact.html", args)
            return

        self.response.headers['Content-Type'] = 'text/html'
        self.process("contact.ok.html")        

application = webapp.WSGIApplication(
                                     [('/contact.php', ContactPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
