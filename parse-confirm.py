#!/usr/bin/env python3
import sys
import json

from spamcop.response import SpamCopConfirmFormFinder

scrff = SpamCopConfirmFormFinder()
payload = scrff.find(open(sys.argv[1]).read())
print(json.dumps(payload, indent=4, sort_keys=True))
