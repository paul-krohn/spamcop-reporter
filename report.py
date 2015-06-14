#!/usr/bin/env python3

import logging
logging.basicConfig(level=logging.DEBUG)


from spamcop.client import SpamCopClient


client = SpamCopClient()
# client._show_cookie_file()
