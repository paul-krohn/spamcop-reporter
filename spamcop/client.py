import configparser
import logging
import os
import requests
import json


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