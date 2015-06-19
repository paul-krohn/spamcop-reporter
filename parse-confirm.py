#!/usr/bin/env python3
import sys
import json

from spamcop.response import SpamCopFinder

finder = SpamCopFinder()
payload = finder.confirm_form(open(sys.argv[1]).read())
print(json.dumps(payload, indent=4, sort_keys=True))
