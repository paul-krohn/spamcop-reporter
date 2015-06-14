import configparser
import logging
import os
# from pickle import Pickler, Unpickler
import pickle
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

        # check the config for a cookie file over-ride
        self.cookie_file = "~/.spamcop_cookies"
        if "Paths" in self.cf.sections():
            try:
                self.cookie_file = self.cf.get("Paths", "cookie_file")
            except configparser.NoOptionError:
                pass
        self._login()

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

        login_response = s.post("https://www.spamcop.net/mcgi", data=payload, allow_redirects=False)
        logging.debug("login initiation request response code: %s" % login_response.status_code)

        confirm_response = s.post(login_response.headers['location'], allow_redirects=False)
        logging.debug("login confirmation request response code: %s" % confirm_response.status_code)

        self._save_cookies(s.cookies)
        return s

    def _save_cookies(self, mmmm_cookies):
        cookie_file_h = open(os.path.expanduser(self.cookie_file), 'w')
        cookie_file_h.write(json.dumps(requests.utils.dict_from_cookiejar(mmmm_cookies)))
        print(json.dumps(requests.utils.dict_from_cookiejar(mmmm_cookies)))
        cookie_file_h.close()
