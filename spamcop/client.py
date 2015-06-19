import configparser
import logging
import os
import requests
import json
import time

from spamcop.response import SpamCopFinder

class SpamCopClient:

    def __init__(self, config_file="~/.spamcop"):
        """
        init method checks for a valid login cookie, and attempt to log in if you don't have one
        :return:
        """
        # does the config file exist?
        self.cf = configparser.ConfigParser()
        self.cf.read(os.path.expanduser(config_file))
        self.base_url = "https://www.spamcop.net/"
        self.login_url = "%smcgi" % self.base_url
        self.reporting_url = "%ssc" % self.base_url

        # check the config for a cookie file over-ride
        self.cookie_file = "~/.spamcop_cookies"
        if "Paths" in self.cf.sections():
            try:
                self.cookie_file = self.cf.get("Paths", "cookie_file")
            except configparser.NoOptionError:
                pass
        self.cookie_file = os.path.expanduser(self.cookie_file)
        # attempt to load cookies
        if self._load_cookies():
            pass
        # else log in
        else:
            self._login()
        print(self.cookie_jar)

    def _login(self):
        """
        Using credentials from the config file, send the login form to
        spamcop and store the returned cookie in self.cookie_file.
        :return: requests.Session
        """

        payload = {
            "action": "cookielogin",
            "username": self.cf.get("Auth", "username"),
            "password": self.cf.get("Auth", "password"),
            "duration": "+1y"
        }

        logging.debug(payload)
        s = requests.Session()

        login_response = s.post(self.login_url, data=payload, allow_redirects=False)
        logging.debug("login initiation request (to %s) response code: %s" %
                      (self.login_url, login_response.status_code))

        confirm_response = s.post(login_response.headers['location'], allow_redirects=False)
        logging.debug("login confirmation request response code: %s" % confirm_response.status_code)

        self._save_cookies(s.cookies)
        return s

    def _load_cookies(self):
        """
        check for and load a cookie file, return false if the file does
        not exist or is not json
        :return:
        """
        logging.debug("loading cookies from: %s" % self.cookie_file)
        if os.path.isfile(self.cookie_file):
            try:
                self.cookie_jar = requests.utils.cookiejar_from_dict(
                    json.load(
                        open(self.cookie_file)
                    )
                )
                return True
            except:
                # if the file isn't JSON, we'll log in & over-write later
                return False
        else:
            return False

    def _save_cookies(self, cookies):
        cookie_file_h = open(os.path.expanduser(self.cookie_file), 'w')
        cookie_file_h.write(json.dumps(requests.utils.dict_from_cookiejar(cookies)))
        print(json.dumps(requests.utils.dict_from_cookiejar(cookies)))
        cookie_file_h.close()

    def report(self, path_to_spam_mail_file):
        """
        Report a spam, and hopefully press the
        confirm button as well
        :param path_to_spam_mail_file:
        :return:
        """
        logging.debug("reporting spam from file %s" % path_to_spam_mail_file)
        reporting_session = requests.Session()
        reporting_session.cookies = self.cookie_jar

        payload = dict()
        payload['action'] = "submit"
        payload['oldverbose'] = "0"
        payload['spam'] = open(path_to_spam_mail_file).read()
        # this looks like a way of getting more diagnostic info from
        # spamcop, so why not?
        payload['verbose'] = "1"

        logging.debug("the reporting payload spam is: %s" % payload['spam'])

        report_response = reporting_session.post(self.reporting_url, data=payload, allow_redirects=False)
        logging.debug("report response code is: %s" % report_response.status_code)
        logging.debug("report response text is: %s" % report_response.text)
        report_redirect_response = reporting_session.get(report_response.headers["location"])
        logging.debug("redirect request to %s resulted in %s" %
                      (report_response.headers["location"], report_redirect_response.status_code))
        logging.debug("and the text is: %s" % report_redirect_response.text)
        # now detect if a meta refresh tag is present, and if so, the time
        refresh = SpamCopFinder.meta_refresh_seconds(report_redirect_response.text)
        if refresh:
            time.sleep(float(refresh))
            # now GET the ... same URL?
            logging.debug("getting the same (?) url again: %s" % report_response.headers["location"])
            after_interstitial_response = reporting_session.get(report_response.headers["location"])
            logging.debug("post-interstitial status code/response: %s/%s" %
                          (after_interstitial_response.status_code, after_interstitial_response.text))

        else:
            logging.debug("you are paid and/or on the confirm page already?")
            pass

# print ("the refresh is: %s" % refresh)


"""
        <p><form method="post" action="/sc" name="submitspam"
  onsubmit="return formval(50000);"
  enctype="multipart/form-data"
  accept="text/plain"
  accept-charset="ISO-8859-1">
<input type="hidden" name="action" value="submit">
<input type="hidden" name="oldverbose" value="0">
Forward your spam to: <a href="mailto:submit.lvQdBnQemD2ZcN0l@spam.spamcop.net">
submit.lvQdBnQemD2ZcN0l@spam.spamcop.net</a> or:
<br>
Paste entire spam (headers, blank line, body) - or - single address (one line only):
<br>
<textarea class="widetext" name="spam" rows=7 cols=80
 wrap="off"></textarea><br>

<input type="submit" name="x1" value="Process Spam">
<input type="reset" name="x2" value="Clear Form">
<input type="checkbox" name="verbose" value=1>Show technical details</form>
<p>

"""
